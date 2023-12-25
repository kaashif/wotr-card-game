from dataclasses import dataclass
from wotr.enums import Faction, CardType, CharacterClass
from wotr.named import Named


@dataclass
class FactionCard(Named):
    faction: Faction
    card_type: CardType
    title: str
    base_battleground_attack: int = 0
    base_battleground_defense: int = 0
    base_leadership_attack: int = 0
    base_leadership_defense: int = 0
    allowed_paths: list[int] = []
    path_combat_icons: int = 0
    allowed_wielders: list[CharacterClass] = []
    just_played: bool = True
    items: list["FactionCard"] = []

    def name(self) -> str:
        return self.title
