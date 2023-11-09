from dataclasses import dataclass

@dataclass
class Battleground:
    side: Side
    defense_icons: int
    defending_faction_icons: list[Faction]
    title: str
    attacking_faction_icons: list[Faction]
    victory_point_value: int

    shadow_cards: list[FactionCard]
    free_cards: list[FactionCard]

    def activate():
        pass

    def resolve():
        pass