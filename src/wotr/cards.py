from typing import Callable

from wotr.faction_card import FactionCard
from wotr.enums import Faction, PlayerCharacter

faction_to_cards = {
    faction: [] for faction in Faction
}

character_to_factions = {
    PlayerCharacter.FRODO: [
        Faction.DWARF,
        Faction.HOBBIT,
        Faction.ROHAN,
        Faction.WIZARD,
    ],
    PlayerCharacter.WITCH_KING: [
        Faction.MORDOR
    ],
    PlayerCharacter.ARAGORN: [
        Faction.DUNEDAIN,
        Faction.ELF,
    ],
    PlayerCharacter.SARUMAN: [
        Faction.ISENGARD,
        Faction.MONSTROUS,
        Faction.SOUTHRON,
    ]
}

def get_cards_for_character(character: PlayerCharacter) -> list[FactionCard]:
    factions = character_to_factions[character]

    return sum([faction_to_cards[faction] for faction in factions], [])

def card(faction: Faction) -> Callable[[type], type]:
    def decorator(card_class: type) -> type:
        faction_to_cards[faction].append(card_class())
        return card_class
    return decorator