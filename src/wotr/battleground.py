from dataclasses import dataclass

from wotr.enums import CardType, Side, Faction
from wotr.faction_card import FactionCard
from wotr.named import Named


@dataclass
class Battleground(Named):
    title: str
    side: Side
    defense_icons: int
    defending_faction_icons: list[Faction]
    attacking_faction_icons: list[Faction]
    victory_point_value: int
    cards: list[FactionCard]

    def card_is_playable(self, card: FactionCard) -> bool:
        # Only armies and characters can be played to battlegrounds
        # Given that the card type is right, the battleground faction needs to match
        return (
            card.card_type in [CardType.ARMY, CardType.CHARACTER]
            and card.faction
            in self.attacking_faction_icons + self.defending_faction_icons
        )

    def name(self) -> str:
        return self.title


def make_battleground(
    title: str,
    side: Side,
    defense_icons: int,
    defending_faction_icons: list[Faction],
    attacking_faction_icons: list[Faction],
    victory_point_value: int,
) -> Battleground:
    return Battleground(
        title,
        side,
        defense_icons,
        defending_faction_icons,
        attacking_faction_icons,
        victory_point_value,
        [],
    )
