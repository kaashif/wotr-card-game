from dataclasses import dataclass

from wotr.faction_card import FactionCard


@dataclass
class Reserve:
    cards: list[FactionCard]
