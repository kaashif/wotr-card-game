from dataclasses import dataclass
from wotr.enums import Faction, CardType, CharacterClass
from wotr.named import Named
from wotr.util import indent


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
    card_text: str

    def name(self) -> str:
        return self.title

    def __str__(self) -> str:
        card_string = f"{self.title} ({self.faction.name}, {self.card_type.name})\n"
        card_string += f"Just Played: {self.just_played}\n"

        if self.card_text != "":
            card_string += f"Card Text: {self.card_text}\n"

        if self.base_battleground_attack != 0:
            card_string += (
                f"Base Battleground Attack: {self.base_battleground_attack}\n"
            )

        if self.base_battleground_defense != 0:
            card_string += (
                f"Base Battleground Defense: {self.base_battleground_defense}\n"
            )

        if self.base_leadership_attack != 0:
            card_string += f"Base Leadership Attack: {self.base_leadership_attack}\n"

        if self.base_leadership_defense != 0:
            card_string += f"Base Leadership Defense: {self.base_leadership_defense}\n"

        if len(self.allowed_paths) > 0:
            card_string += f"Allowed Paths: {self.allowed_paths}\n"

        if self.path_combat_icons != 0:
            card_string += f"Path Combat Icons: {self.path_combat_icons}\n"

        if len(self.allowed_wielders) > 0:
            card_string += f"Allowed Wielders: {self.allowed_wielders}\n"

        if len(self.items) > 0:
            card_string += (
                f"Items:\n{'\n'.join(indent(str(item), 2) for item in self.items)}\n"
            )

        return card_string
