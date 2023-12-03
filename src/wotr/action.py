from typing import Callable
import itertools

from wotr.player import Player
from wotr.state import State

# Something you can perform during your turn
class Action:
    def __init__(self, description: str, executor: Callable) -> None:
        self.description = description
        self.executor = executor

    def __str__(self) -> str:
        return self.description
    
    def execute(self) -> None:
        self.executor()

def list_play_card_actions(state: State, player: Player) -> list[Action]:
    pass 

def list_move_from_reserve_actions(state: State, player: Player) -> list[Action]:
    pass 

def list_cycle_actions(state: State, player: Player) -> list[Action]:
    pass

def list_winnow_actions(state: State, player: Player) -> list[Action]:
    pass 

def list_on_card_actions(state: State, player: Player) -> list[Action]:

def list_ring_token_actions(state: State, player: Player) -> list[Action]:
    if player.used_ring_token:
        return []
    else:
        return [
            Action(
                "use ring token",
                player.use_ring_token
            )
        ]

def get_pass_action(player: Player) -> list[Action]:
    return [Action(
        "pass",
        player.pass_turn
    )]
    
def list_actions(state: State, player: Player) -> list[Action]:
    return list(itertools.chain(
        list_play_card_actions(state, player),
        list_move_from_reserve_actions(state, player),
        list_cycle_actions(state, player),
        list_winnow_actions(state, player),
        list_on_card_actions(state, player),
        list_ring_token_actions(state, player),
        get_pass_action(player),
    ))