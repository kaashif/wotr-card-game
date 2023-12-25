from dataclasses import dataclass
from typing import Callable

from wotr.enums import CardType, Side, Faction
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
    activate_callback: Callable[["Battleground", State], None]

    def card_is_playable(self, card: FactionCard) -> bool:
        # Only armies and characters can be played to battlegrounds
        # Given that the card type is right, the battleground faction needs to match
        return card.card_type in [CardType.ARMY, CardType.CHARACTER] \
            and card.faction in self.attacking_faction_icons + self.defending_faction_icons

    def activate(self, state: State) -> None:
        self.activate_callback(self, state) 

class BattlegroundDeck(Deck):
    def __init__(self, side: Side):
        super().__init__([battleground for battleground in all_battlegrounds if battleground.side == side])
