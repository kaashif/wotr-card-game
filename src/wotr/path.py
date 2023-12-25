from dataclasses import dataclass
from wotr.enums import CardType

from wotr.faction_card import FactionCard
from wotr.named import Named
from wotr.util import indent


@dataclass
class Path(Named):
    title: str
    path_number: int
    defense_icons: int
    victory_point_value: int
    cards: list[FactionCard]
    card_text: str

    def card_is_playable(self, card: FactionCard) -> bool:
        return (
            card.card_type == CardType.CHARACTER
            and self.path_number in card.allowed_paths
        )

    def name(self) -> str:
        return self.title

    # TODO: Print a summary of who's winning the path.
    def __str__(self) -> str:
        card_string = f"{self.title} (Path {self.path_number})\n"
        card_string += f"Defense Icons: {self.defense_icons}\n"
        card_string += f"Victory Point Value: {self.victory_point_value}\n"

        if self.card_text != "":
            card_string += f"Card Text: {self.card_text}\n"

        if len(self.cards) > 0:
            card_string += f"Cards:\n{'\n'.join(indent(f'{card.title} ({card.faction})', 2) for card in sorted(self.cards, key=lambda card: card.faction))}\n"

        return card_string


def make_path(
    title: str,
    path_number: int,
    defense_icons: int,
    victory_point_value: int,
    card_text: str,
) -> Path:
    return Path(title, path_number, defense_icons, victory_point_value, [], card_text)
