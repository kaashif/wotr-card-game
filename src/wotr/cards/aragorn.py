from wotr.enums import Faction
from wotr.cards import register_army

# TODO: +2 attack/defense while supporting Aragorn/Strider
register_army(
    title="Dead Men of Dunharrow",
    faction=Faction.DUNEDAIN,
    base_battleground_attack=0,
    base_battleground_defense=0,
)

# TODO: +1 defense token on Dol Amroth
register_army(
    title="Knights of Dol Amroth",
    faction=Faction.DUNEDAIN,
    base_battleground_attack=1,
    base_battleground_defense=1,
)