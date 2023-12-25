from dataclasses import dataclass
from wotr.enums import CardType

from wotr.faction_card import FactionCard
from wotr.named import Named


@dataclass
class Path(Named):
    title: str
    path_number: int
    defense_icons: int
    victory_point_value: int
    cards: list[FactionCard]

    def card_is_playable(self, card: FactionCard) -> bool:
        return (
            card.card_type == CardType.CHARACTER
            and self.path_number in card.allowed_paths
        )

    def name(self) -> str:
        return self.title


def make_path(
    title: str, path_number: int, defense_icons: int, victory_point_value: int
) -> Path:
    return Path(title, path_number, defense_icons, victory_point_value, [])
