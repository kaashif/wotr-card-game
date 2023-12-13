import random
from dataclasses import dataclass
from wotr.deck import Deck

from wotr.faction_card import FactionCard
from wotr.state import State
from wotr.paths import all_paths

@dataclass
class Path:
    defense_icons: int
    title: str
    path_number: int
    victory_point_value: int

    cards: list[FactionCard]

    def activate(self, state: State) -> None:
        pass

class PathDeck(Deck[Path]):
    def __init__(self):
        super().__init__(all_paths)

    def draw_path(self, current_path: int) -> Path:
        eligible_paths = [path for path in self.cards if path.path_number == current_path]
        chosen_path = random.choice(eligible_paths)
        self.cards = [path for path in self.cards if path is not chosen_path]
        return chosen_path