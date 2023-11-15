from dataclasses import dataclass

from wotr.enums import Side, Faction
from wotr.faction_card import FactionCard
from wotr.deck import Deck


@dataclass
class Battleground:
    side: Side
    defense_icons: int
    defending_faction_icons: list[Faction]
    title: str
    attacking_faction_icons: list[Faction]
    victory_point_value: int

    cards: list[FactionCard]

    def activate():
        pass

    def resolve():
        pass

all_battlegrounds: list[Battleground] = []

class BattlegroundDeck(Deck):
    def __init__(self, side: Side):
        super().__init__([battleground for battleground in all_battlegrounds if battleground.side == side])
