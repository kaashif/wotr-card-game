from dataclasses import dataclass
from wotr.enums import Faction, CardType, CharacterClass
from wotr.named import Named


@dataclass
class FactionCard(Named):
    title: str
    faction: Faction
    card_type: CardType
    base_battleground_attack: int
    base_battleground_defense: int
    base_leadership_attack: int
    base_leadership_defense: int
    allowed_paths: list[int]
    path_combat_icons: int
    allowed_wielders: list[CharacterClass]
    just_played: bool
    items: list["FactionCard"]

    def name(self) -> str:
        return self.title
