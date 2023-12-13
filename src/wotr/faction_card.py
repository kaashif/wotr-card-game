import json
from dataclasses import dataclass
import dataclasses
from wotr.battleground import Battleground

from wotr.enums import Faction, CardType, CharacterClass
from wotr.path import Path
from wotr.state import PlayLocation, State

@dataclass
class FactionCard:
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

    def when_played(self, state: State) -> None:
        pass

    def when_forsaken_from_top_of_deck(self, state: State) -> None:
        pass

    def when_played_to_location(self, state: State, location: PlayLocation) -> None:
        pass

    def battleground_attack(self) -> int:
        return self.base_battleground_attack

    def battleground_defense(self) -> int:
        return self.base_battleground_defense

    def card_draw_bonus(self) -> int:
        return 0

    def carryover_limit_bonus(self) -> int:
        return 0

    def add_item(self, item: "FactionCard") -> None:
        self.items.append(item)

    def is_playable_to_battleground(self, battleground: Battleground) -> bool:
        # Only armies and characters can be played to battlegrounds
        if self.card_type not in [CardType.ARMY, CardType.CHARACTER]:
            return False

        # Given that the card type is right, the battleground faction needs to match
        return self.faction in battleground.attacking_faction_icons + battleground.defending_faction_icons

    def is_playable_to_path(self, path: Path) -> bool:
        return self.card_type == CardType.CHARACTER and \
            path.path_number in self.allowed_paths

    def can_do_action(self, state: State) -> bool:
        return False

    def perform_card_action(self, state: State) -> None:
        pass
