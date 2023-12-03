from dataclasses import dataclass
from typing import Iterable
from wotr.battleground import Battleground, BattlegroundDeck
from wotr.path import Path, PathDeck
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import Side

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

    game_round: int = 1
    current_path_number: int = 1

    active_battleground: Battleground | None = None
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
        return self.current_path_number > 9:
        # TODO: also do the difference greater than 10 one