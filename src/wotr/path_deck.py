import random
from wotr.deck import Deck
from wotr.path import Path, make_path

all_paths: list[Path] = [
    make_path(
        "Bag End",
        path_number=1,
        defense_icons=0,
        victory_point_value=1,
    ),
]


class PathDeck(Deck[Path]):
    def __init__(self, paths: list[Path]):
        self.paths = paths

    def draw_path(self, current_path: int) -> Path:
        eligible_paths = [
            path for path in self.cards if path.path_number == current_path
        ]
        chosen_path = random.choice(eligible_paths)
        self.cards = [path for path in self.cards if path is not chosen_path]
        return chosen_path
