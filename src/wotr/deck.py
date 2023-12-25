from dataclasses import dataclass
from typing import TypeVar, Generic
import random

T = TypeVar("T")


@dataclass
class Deck(Generic[T]):
    cards: list[T]

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def draw(self) -> T:
        return self.cards.pop(0)

    def add_to_bottom(self, card: T) -> None:
        self.cards.append(card)

    def shuffle_into(self, other: "Deck[T]") -> None:
        other.cards += self.cards
        self.cards = []
        other.shuffle()

    def take(self, card_title: str) -> None:
        pass

    def shuffle(self) -> None:
        random.shuffle(self.cards)
