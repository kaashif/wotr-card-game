from dataclasses import dataclass

@dataclass
class FactionCard:
    faction: Faction
    card_type: CardType
    base_battleground_attack: int
    base_battleground_defense: int
    base_leadership_attack: int
    base_leadership_defense: int
    allowed_paths: list[int]
    path_combat_icons: int
    title: str
    allowed_wielders: list[CharacterClass]

    def play_to_battleground():
        pass

    def play_to_path():
        pass
    
    def play_item_to_wielder():
        pass

    def play_event():
        pass

    def play_to_reserve():
        pass

    def forsake():
        pass

    def forsake_from_top_of_deck():
        pass

    def eliminate():
        pass

    def reserve_action():
        pass

    def path_action():
        pass

    def item_action():
        pass

    def battleground_attack() -> int:
        pass

    def battleground_defense() -> int:
        pass