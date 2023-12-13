from typing import Callable
from wotr.enums import PlayerCharacter
from wotr.faction_card import FactionCard
from wotr.path import Path
from wotr.state import State


all_paths: list[Path] = []

def path(title: str, path_number: int, defense_icons: int, victory_point_value: int) -> Callable:
    def create_path_given_activate(activate: Callable[[State], None]) -> None:
        path_object = Path(path_number, defense_icons, title, victory_point_value, [])
        path_object.activate = activate
        all_paths.append(path)
    return create_path_given_activate

@path("Bag End", path_number=1, defense_icons=0, victory_point_value=1)
def bag_end(state: State) -> None:
    state.character_to_player[PlayerCharacter.FRODO].draw(2)