import json
from dataclasses import dataclass
import dataclasses
from wotr.battleground import Battleground

from wotr.enums import Faction, CardType, CharacterClass
from wotr.path import Path

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

    def play_to_battleground(self):
        pass

    def play_to_path(self):
        pass
    
    def play_item_to_wielder(self):
        pass

    def play_event(self):
        pass

    def play_to_reserve(self):
        pass

    def forsake(self):
        pass

    def forsake_from_top_of_deck(self):
        pass

    def eliminate(self):
        pass

    def reserve_action(self):
        pass

    def path_action(self):
        pass

    def item_action(self):
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

def choose_faction_card(cards: list[FactionCard]) -> FactionCard:
    for i in range(0, len(cards)):
        card = cards[i]
        print(f"{i}:\n{json.dumps(dataclasses.asdict(card), indent=2)}")

    chosen_i = int(input("Choose a card index: "))

    return cards[chosen_i]
        