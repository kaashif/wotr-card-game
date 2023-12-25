from wotr.faction_card import FactionCard
from wotr.enums import CardType, Faction, PlayerCharacter

faction_to_cards: dict[Faction, list[FactionCard]] = {
    faction: [] for faction in Faction
}

character_to_factions = {
    PlayerCharacter.FRODO: [
        Faction.DWARF,
        Faction.HOBBIT,
        Faction.ROHAN,
        Faction.WIZARD,
    ],
    PlayerCharacter.WITCH_KING: [Faction.MORDOR],
    PlayerCharacter.ARAGORN: [
        Faction.DUNEDAIN,
        Faction.ELF,
    ],
    PlayerCharacter.SARUMAN: [
        Faction.ISENGARD,
        Faction.MONSTROUS,
        Faction.SOUTHRON,
    ],
}


def get_cards_for_character(character: PlayerCharacter) -> list[FactionCard]:
    factions = character_to_factions[character]

    return sum([faction_to_cards[faction] for faction in factions], [])


def register_card(card: FactionCard) -> None:
    faction_to_cards[card.faction].append(card)


def register_army(
    title: str,
    faction: Faction,
    base_battleground_attack: int,
    base_battleground_defense: int,
    card_text: str = "",
) -> None:
    register_card(
        FactionCard(
            title=title,
            faction=faction,
            card_type=CardType.ARMY,
            base_battleground_attack=base_battleground_attack,
            base_battleground_defense=base_battleground_defense,
            base_leadership_attack=0,
            base_leadership_defense=0,
            allowed_paths=[],
            path_combat_icons=0,
            allowed_wielders=[],
            just_played=False,
            items=[],
            card_text=card_text,
        )
    )
