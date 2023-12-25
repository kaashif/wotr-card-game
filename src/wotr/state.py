import itertools

from dataclasses import dataclass
from typing import Iterable, Sequence, TypeAlias
from wotr.battleground import Battleground, BattlegroundDeck
from wotr.faction_card import FactionCard
from wotr.path import Path, PathDeck
from wotr.reserve import Reserve
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import CardType, Faction, PlayerCharacter, Side
from wotr.cards import character_to_factions

class AsEvent:
    pass

# You can play a card to reserve, path combat, battleground combat,
# onto another card as an item, or it's an event and resolves, then is eliminated.
PlayLocation: TypeAlias = Reserve | Path | Battleground | FactionCard | AsEvent

@dataclass
class State:
    shadow_scoring_area: ShadowScoringArea
    free_scoring_area: FreeScoringArea
    
    frodo_player: Player
    witch_king_player: Player
    aragorn_player: Player
    saruman_player: Player

    shadow_battleground_deck: BattlegroundDeck
    free_battleground_deck: BattlegroundDeck

    path_deck: PathDeck
    
    active_battlegrounds: list[Battleground]

    game_round: int = 1
    current_path_number: int = 1

    active_path: Path | None = None

    def character_to_player(self, character: PlayerCharacter) -> Player:
        map = {
            PlayerCharacter.FRODO: self.frodo_player,
            PlayerCharacter.WITCH_KING: self.witch_king_player,
            PlayerCharacter.ARAGORN: self.aragorn_player,
            PlayerCharacter.SARUMAN: self.saruman_player,
        }

        return map[character]

    def faction_to_player(self, faction: Faction) -> Player:
        if faction in [Faction.DWARF, Faction.HOBBIT, Faction.ROHAN, Faction.WIZARD]:
            return self.frodo_player
        
        if faction in [Faction.MORDOR]:
            return self.witch_king_player
        
        if faction in [Faction.DUNEDAIN, Faction.ELF]:
            return self.aragorn_player
        
        if faction in [Faction.ISENGARD, Faction.MONSTROUS, Faction.SOUTHRON]:
            return self.saruman_player

        raise Exception(f"Unknown faction {faction}")

    def all_players(self) -> list[Player]:
        return list(self.character_to_player(character) for character in PlayerCharacter)

    def get_side_for_round(self) -> Side:
        return [Side.FREE, Side.SHADOW][(self.game_round-1) % 2]

    def player_turns(self) -> Iterable[Player]:
        round_index = self.game_round - 1
        current_player_index = round_index % 4

        while True:
            yield self.all_players()[current_player_index]
            current_player_index += 1


    def end_game(self) -> None:
        print("GAME OVER!")
        if self.shadow_scoring_area.total_victory_points() >= self.free_scoring_area.total_victory_points():
            print("Shadow wins!")
        else:
            print("Free Peoples win!")
        
        print(self.shadow_scoring_area)
        print(self.free_scoring_area)

    
    def get_total_points_for_side(self, side: Side) -> int:
        if side == Side.FREE:
            return self.free_scoring_area.total_victory_points() + [self.frodo_player.used_ring_token, self.aragorn_player.used_ring_token].count(False)
        else:
            return self.shadow_scoring_area.total_victory_points() + [self.witch_king_player.used_ring_token, self.saruman_player.used_ring_token].count(False)


    def is_game_over(self) -> bool:
        return self.current_path_number > 9
        # TODO: also do the difference greater than 10 one
    
    def get_playable_locations(self, player: Player, card: FactionCard) -> Sequence[PlayLocation]:
        match card.card_type:
            case CardType.ARMY:
                # Armies can be played to reserve or battlegrounds
                return [player.reserve] + [
                    battleground for battleground in self.active_battlegrounds
                    if battleground.card_is_playable(card)
                ]
            case CardType.CHARACTER:
                # Characters can be played to reserve, path, battleground
                return [player.reserve] + [
                    path for path in ([self.active_path] if self.active_path is not None else [])
                    if card.is_playable_to_path(path)
                ] + [
                    battleground for battleground in self.active_battlegrounds
                    if battleground.card_is_playable(card)
                ]
            case CardType.EVENT:
                # Events aren't really played "to" anywhere, but they're still played
                return [AsEvent()]

            case CardType.ITEM:
                # Items can only be played to their wielders
                # Wielders could be anywhere that a character can be played to:
                # reserve, path, or battleground.
                return [
                    wielder for wielder in itertools.chain(
                        itertools.chain.from_iterable(b.cards for b in self.active_battlegrounds),

                        # TODO: There can't actually be NO active path, disallow it statically
                        self.active_path.cards if self.active_path is not None else [],

                        # Note: One player can play items to characters of a different player
                        itertools.chain.from_iterable(p.reserve.cards for p in self.all_players())
                    )
                ]

    def move_card_to_location(self, card: FactionCard, location: PlayLocation) -> None:
        match location:
            case Reserve():
                location.cards.append(card)
            case Path():
                location.cards.append(card)
            case Battleground():
                location.cards.append(card)
            case FactionCard():
                location.add_item(card)
 

    def play_card(self, player: Player, card: FactionCard, location: PlayLocation) -> None:
        player.hand.remove(card)
        self.move_card_to_location(card, location)

        # Note: card.when_played may result in a choice for the player!
        # e.g. Legolas: When played you may take the Bow of Galadhrim from your draw deck into hand.
        card.when_played(self)

        # When played to a specific location, the card may have a special effect.
        card.when_played_to_location(self, location)

        if isinstance(location, AsEvent):
            player.eliminated_pile.add_to_bottom(card)

    def move_card_from_reserve(self, player: Player, card: FactionCard, location: PlayLocation) -> None:
        player.reserve.cards.remove(card)

        self.move_card_to_location(card, location)

        # The when_played doesn't trigger again because the card was already played to reserve.
        # But the when_played_to_location does trigger, because the location is changing.
        card.when_played_to_location(self, location)

    def find_all_active_cards_for_player(self, player: Player) -> list[FactionCard]:
        # All cards except item cards, since item cards live on other cards
        played_cards_except_items = itertools.chain(
            player.reserve.cards,
            itertools.chain.from_iterable(b.cards for b in self.active_battlegrounds),
            self.active_path.cards if self.active_path is not None else []
        )

        # Any card may be a character card with items on it
        item_cards = itertools.chain.from_iterable(
            card.items for card in played_cards_except_items
        )

        return list(itertools.chain(played_cards_except_items, item_cards))

    def cards_with_doable_actions_for_player(self, player: Player) -> list[FactionCard]:
        return [
            card for card in self.find_all_active_cards_for_player(player)
            if card.can_do_action(self)
        ]

    def perform_card_action(self, card: FactionCard) -> None:
        # I don't think any card has multiple actions.
        # Lots of card actions result in choices.
        card.perform_card_action(self)

    
    def get_card_owner(self, card: FactionCard) -> Player:
        for character, factions in character_to_factions.items():
            if card.faction in factions:
                return self.character_to_player(character)
        
        raise Exception(f"Could not find owner for card {card}")

    def eliminate_card_wherever_it_is(self, card: FactionCard) -> None:
        for player in self.all_players():
            if card in player.reserve.cards:
                player.reserve.cards.remove(card)

            if card in player.hand:
                player.hand.remove(card)

        for battleground in self.active_battlegrounds:
            if card in battleground.cards:
                battleground.cards.remove(card)

        if self.active_path is not None and card in self.active_path.cards:
            self.active_path.cards.remove(card)
        
        self.get_card_owner(card).eliminated_pile.add_to_bottom(card)

    
    def get_battleground_by_name(self, name: str) -> Battleground:
        for battleground in itertools.chain(self.active_battlegrounds, self.free_scoring_area.battlegrounds, self.shadow_scoring_area.battlegrounds):
            if battleground.title == name:
                return battleground

        raise Exception(f"No battleground with name {name}")

    def resolve_battlegrounds(self) -> None:
        # TODO
        pass

    def resolve_active_path(self) -> None:
        # TODO
        pass