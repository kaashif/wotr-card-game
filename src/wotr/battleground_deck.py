from wotr.battleground import Battleground, make_battleground
from wotr.deck import Deck
from wotr.enums import Faction, Side

all_battlegrounds: list[Battleground] = [
    make_battleground(
        title="Helms Deep",
        side=Side.FREE,
        defense_icons=2,
        defending_faction_icons=[Faction.WIZARD, Faction.ROHAN],
        attacking_faction_icons=[Faction.ISENGARD],
        victory_point_value=2,
    ),
]


class BattlegroundDeck(Deck):
    def __init__(self, battlegrounds: list[Battleground]):
        self.battlegrounds = battlegrounds


def get_battlegrounds_for_side(side: Side) -> list[Battleground]:
    return [
        battleground for battleground in all_battlegrounds if battleground.side == side
    ]
