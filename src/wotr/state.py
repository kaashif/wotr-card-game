import itertools

from dataclasses import dataclass
from typing import Iterable, Sequence
from wotr.battleground import Battleground, BattlegroundDeck
from wotr.faction_card import FactionCard
from wotr.path import Path, PathDeck
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import CardType, Faction, Side

class Reserve:
    pass

class AsEvent:
    pass

# You can play a card to reserve, path combat, battleground combat,
# onto another card as an item, or it's an event and resolves, then is eliminated.
PlayLocation = Reserve | Path | Battleground | FactionCard | AsEvent

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


    def all_players(self) -> list[Player]:
        return [
            self.frodo_player,
            self.witch_king_player,
            self.aragorn_player,
            self.saruman_player,
        ]

    def starting_side(self) -> Side:
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
    
    def get_playable_locations(self, card: FactionCard) -> Sequence[PlayLocation]:
        match card.card_type:
            case CardType.ARMY:
                # Armies can be played to reserve or battlegrounds
                return [Reserve()] + [
                    battleground for battleground in self.active_battlegrounds
                    if card.is_playable_to_battleground(battleground)
                ]
            case CardType.CHARACTER:
                # Characters can be played to reserve, path, battleground
                return [Reserve()] + [
                    path for path in ([self.active_path] if self.active_path is not None else [])
                    if card.is_playable_to_path(path)
                ] + [
                    battleground for battleground in self.active_battlegrounds
                    if card.is_playable_to_battleground(battleground)
                ]
            case CardType.EVENT:
                # Events aren't really played "to" anywhere
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

    def play_card(self, card: FactionCard, location: PlayLocation) -> None:
        # TODO
        pass

    def move_card_from_reserve(self, card: FactionCard, location: PlayLocation) -> None:
        # TODO
        pass


    def cards_with_doable_actions_for(self, player: Player) -> list[FactionCard]:
        # TODO
        pass

    def perform_card_action(self, card: FactionCard) -> None:
        # TODO
        pass

