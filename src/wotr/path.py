from dataclasses import dataclass

@dataclass
class Path:
    defense_icons: int
    title: str
    path_number: int
    victory_point_value: int

    shadow_cards: list[FactionCard]
    free_cards: list[FactionCard]

    def activate():
        pass

    def resolve():
        pass