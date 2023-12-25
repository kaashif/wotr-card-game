from wotr.cards import register_army
from wotr.enums import Faction

register_army(
    "Devilry of Saruman",
    Faction.ISENGARD,
    base_battleground_attack=3,
    base_battleground_defense=0,
)

register_army(
    "Fighting Uruk-Hai",
    Faction.ISENGARD,
    base_battleground_attack=1,
    base_battleground_defense=2,
)

register_army(
    "Wolf Riders",
    Faction.ISENGARD,
    base_battleground_attack=2,
    base_battleground_defense=1,
)

for _ in range(2):
    register_army(
        "White Hand Orcs",
        Faction.ISENGARD,
        base_battleground_attack=1,
        base_battleground_defense=1,
    )
