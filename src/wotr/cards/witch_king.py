from wotr.cards import register_army
from wotr.enums import Faction

for _ in range(5):
    register_army(
        "Mordor Orcs",
        Faction.MORDOR,
        base_battleground_attack=1,
        base_battleground_defense=1,
    )