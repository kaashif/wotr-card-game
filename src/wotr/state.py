from dataclasses import dataclass
from typing import Iterable
from wotr.battleground import BattlegroundDeck
from wotr.path import PathDeck
from wotr.state import State
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import Side, PlayerCharacter

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
    current_path: int = 1

    def all_players(self) -> list[Player]:
        return [
            self.frodo_player,
            self.witch_king_player,
            self.aragorn_player,
            self.saruman_player,
        ]

    def starting_side(self) -> Side:
        return [Side.FREE, Side.SHADOW][self.game_round % 2]

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

    def is_game_over(self) -> bool:
        return self.current_path > 9 or \
            (abs(self.shadow_scoring_area.total_victory_points() - self.free_scoring_area.total_victory_points()) >= 10)
