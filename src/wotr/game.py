import itertools

from dataclasses import dataclass
from typing import Iterable, Sequence, TypeAlias
from wotr.battleground import Battleground
from wotr.battleground_deck import BattlegroundDeck
from wotr.decision_type import DecisionType
from wotr.event_handler import Event, EventHandler, EventType
from wotr.faction_card import FactionCard
from wotr.named import Named
from wotr.path import Path
from wotr.path_deck import PathDeck
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
class Game:
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

    event_to_handler: dict[Event, EventHandler]

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
        return list(
            self.character_to_player(character) for character in PlayerCharacter
        )

    def get_side_for_round(self) -> Side:
        return [Side.FREE, Side.SHADOW][(self.game_round - 1) % 2]

    def player_turns(self) -> Iterable[Player]:
        round_index = self.game_round - 1
        current_player_index = round_index % 4

        while True:
            yield self.all_players()[current_player_index]
            current_player_index = (current_player_index + 1) % 4

    def end_game(self) -> None:
        print("GAME OVER!")
        if (
            self.shadow_scoring_area.total_victory_points()
            >= self.free_scoring_area.total_victory_points()
        ):
            print("Shadow wins!")
        else:
            print("Free Peoples win!")

        print(self.shadow_scoring_area)
        print(self.free_scoring_area)

    def get_total_points_for_side(self, side: Side) -> int:
        if side == Side.FREE:
            return self.free_scoring_area.total_victory_points() + [
                self.frodo_player.used_ring_token,
                self.aragorn_player.used_ring_token,
            ].count(False)
        else:
            return self.shadow_scoring_area.total_victory_points() + [
                self.witch_king_player.used_ring_token,
                self.saruman_player.used_ring_token,
            ].count(False)

    def is_game_over(self) -> bool:
        return self.current_path_number > 9
        # TODO: also do the difference greater than 10 one

    def get_playable_locations(
        self, player: Player, card: FactionCard
    ) -> Sequence[PlayLocation]:
        match card.card_type:
            case CardType.ARMY:
                # Armies can be played to reserve or battlegrounds
                return [player.reserve] + [
                    battleground
                    for battleground in self.active_battlegrounds
                    if battleground.card_is_playable(card)
                ]
            case CardType.CHARACTER:
                # Characters can be played to reserve, path, battleground
                return (
                    [player.reserve]
                    + [
                        path
                        for path in (
                            [self.active_path] if self.active_path is not None else []
                        )
                        if path.card_is_playable(card)
                    ]
                    + [
                        battleground
                        for battleground in self.active_battlegrounds
                        if battleground.card_is_playable(card)
                    ]
                )
            case CardType.EVENT:
                # Events aren't really played "to" anywhere, but they're still played
                return [AsEvent()]

            case CardType.ITEM:
                # Items can only be played to their wielders
                # Wielders could be anywhere that a character can be played to:
                # reserve, path, or battleground.
                return [
                    wielder
                    for wielder in itertools.chain(
                        itertools.chain.from_iterable(
                            b.cards for b in self.active_battlegrounds
                        ),
                        # TODO: There can't actually be NO active path, disallow it statically
                        self.active_path.cards if self.active_path is not None else [],
                        # Note: One player can play items to characters of a different player
                        itertools.chain.from_iterable(
                            p.reserve.cards for p in self.all_players()
                        ),
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
                location.items.append(card)

    def play_card(
        self, player: Player, card: FactionCard, location: PlayLocation
    ) -> None:
        player.hand.remove(card)
        self.move_card_to_location(card, location)

        # Note: card.when_played may result in a choice for the player!
        # e.g. Legolas: When played you may take the Bow of Galadhrim from your draw deck into hand.
        self.when_played(card)

        # When played to a specific location, the card may have a special effect.
        self.when_played_to_location(card, location)

        if isinstance(location, AsEvent):
            player.eliminated_pile.add_to_bottom(card)

    def move_card_from_reserve(
        self, player: Player, card: FactionCard, location: PlayLocation
    ) -> None:
        player.reserve.cards.remove(card)

        self.move_card_to_location(card, location)

        # The when_played doesn't trigger again because the card was already played to reserve.
        # But the when_played_to_location does trigger, because the location is changing.
        self.when_played_to_location(card, location)

    def find_all_active_cards_for_player(self, player: Player) -> list[FactionCard]:
        # All cards except item cards, since item cards live on other cards
        played_cards_except_items = itertools.chain(
            player.reserve.cards,
            itertools.chain.from_iterable(b.cards for b in self.active_battlegrounds),
            self.active_path.cards if self.active_path is not None else [],
        )

        # Any card may be a character card with items on it
        item_cards = itertools.chain.from_iterable(
            card.items for card in played_cards_except_items
        )

        return list(itertools.chain(played_cards_except_items, item_cards))

    def cards_with_doable_actions_for_player(self, player: Player) -> list[FactionCard]:
        return [
            card
            for card in self.find_all_active_cards_for_player(player)
            if self.can_do_action(card)
        ]

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
        for battleground in itertools.chain(
            self.active_battlegrounds,
            self.free_scoring_area.battlegrounds,
            self.shadow_scoring_area.battlegrounds,
        ):
            if battleground.title == name:
                return battleground

        raise Exception(f"No battleground with name {name}")

    def resolve_battlegrounds(self) -> None:
        # TODO
        pass

    def resolve_active_path(self) -> None:
        # TODO
        pass

    def when_played(self, card: FactionCard) -> None:
        pass

    def when_forsaken_from_top_of_deck(self, card: FactionCard) -> None:
        pass

    def when_forsaken_from_reserve(self, card: FactionCard) -> None:
        pass

    def when_played_to_location(
        self, card: FactionCard, location: PlayLocation
    ) -> None:
        pass

    def can_do_action(self, card: FactionCard) -> bool:
        return False

    def perform_card_action(self, card: FactionCard) -> None:
        pass

    def forsake_from_draw_deck(self, player: Player) -> None:
        if player.draw_deck.is_empty():
            return

        card = player.draw_deck.draw()

        player.eliminated_pile.add_to_bottom(card)

        # Some cards have effects when forsaken from the top of the deck
        # e.g. when eliminated, cycle instead.
        self.when_forsaken_from_top_of_deck(card)

    def forsake_from_list(self, player: Player, cards: list[FactionCard]) -> None:
        if len(cards) == 0:
            raise Exception("card list is empty!")

        card = player.agent.pick_no_fallback(
            DecisionType.WHICH_CARD_TO_ELIMINATE, cards
        )

        # We cannot just remove card from cards. That works if cards is self.hand
        # or self.reserve.cards, but not if cards is just a list of choices not directly
        # part of the game state. We need to eliminate cards *wherever it really is*.
        player.eliminate_specific(card)

        # p11: If a character is eliminated, all items it is wielding are also eliminated.
        for item in card.items:
            player.eliminated_pile.add_to_bottom(item)

    def forsake(self, player: Player) -> None:
        # p13: When forsaking you can either forsake from the top of the deck, hand, or reserve.
        # p13: You can forsake an item from its wielder.
        # Note: you cannot forsake items or characters from battlegrounds or path.
        possible_forsake_locations = []

        if not player.draw_deck.is_empty() or not player.cycle_pile.is_empty():
            possible_forsake_locations.append("draw deck")

        if len(player.hand) > 0:
            possible_forsake_locations.append("hand")

        if len(player.reserve.cards) > 0:
            possible_forsake_locations.append("reserve")

        reserve_items = [item for card in player.reserve.cards for item in card.items]

        if len(reserve_items) > 0:
            possible_forsake_locations.append("reserve item")

        forsake_location = player.agent.pick_no_fallback(
            DecisionType.WHERE_TO_FORSAKE_FROM, possible_forsake_locations
        )

        if forsake_location == "draw deck":
            self.forsake_from_draw_deck(player)
        elif forsake_location == "hand":
            self.forsake_from_list(player, player.hand)
        elif forsake_location == "reserve":
            self.forsake_from_list(player, player.reserve.cards)
        elif forsake_location == "reserve item":
            self.forsake_from_list(player, reserve_items)

    def get_player_view(self, player: Player) -> str:
        view = ""

        view += f"Player {player.character.name}\n"
        view += f"Hand: {player.hand}\n"
        view += f"Cycle pile: {player.cycle_pile}\n"
        view += f"Eliminated pile: {player.eliminated_pile}\n"

        view += f"Active batlegrounds: {self.active_battlegrounds}\n"
        view += f"Active path: {self.active_path}\n"

        return view

    def trigger_event(self, event_type: EventType, subject: Named) -> None:
        print(f"{event_type.name}\n{subject}")
        self.event_to_handler[Event(event_type, subject.name())](self)
