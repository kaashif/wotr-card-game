import json
from dataclasses import dataclass
import dataclasses

from wotr.enums import Faction, CardType, CharacterClass

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

def choose_faction_card(cards: list[FactionCard]) -> FactionCard:
    for i in range(0, len(cards)):
        card = cards[i]
        print(f"{i}:\n{json.dumps(dataclasses.asdict(card), indent=2)}")

    chosen_i = int(input("Choose a card index: "))

    return cards[chosen_i]
        