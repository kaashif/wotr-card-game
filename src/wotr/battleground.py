from dataclasses import dataclass

from wotr.enums import Side, Faction
from wotr.faction_card import FactionCard
from wotr.deck import Deck
from wotr.state import State
from wotr.battlegrounds import all_battlegrounds

@dataclass
class Battleground:
    side: Side
    defense_icons: int
    defending_faction_icons: list[Faction]
    title: str
    attacking_faction_icons: list[Faction]
    victory_point_value: int

    cards: list[FactionCard]

    def activate(self, state: State) -> None:
        pass

class BattlegroundDeck(Deck):
    def __init__(self, side: Side):
        super().__init__([battleground for battleground in all_battlegrounds if battleground.side == side])
