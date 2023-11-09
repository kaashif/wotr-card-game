from dataclasses import dataclass

@dataclass
class Deck:
    cards: list[FactionCard]

    def draw(self) -> FactionCard:
        pass

    def add_to_bottom(self, card: FactionCard) -> None:
        pass

    def shuffle_into(self, other: Deck) -> None:
        pass

    def take(self, card_title: str) -> None:
        pass