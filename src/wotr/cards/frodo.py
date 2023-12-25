from wotr.cards import register_army
from wotr.enums import Faction

for _ in range(2):
    register_army(
        "Riders of Rohan",
        Faction.ROHAN,
        base_battleground_attack=2,
        base_battleground_defense=1,
    )

register_army(
    "Village Militia",
    Faction.ROHAN,
    base_battleground_attack=1,
    base_battleground_defense=1,
)
