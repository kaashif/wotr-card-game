from dataclasses import dataclass

from wotr.enums import CardType, Side, Faction
from wotr.faction_card import FactionCard
from wotr.named import Named
from wotr.util import indent


@dataclass
class Battleground(Named):
    title: str
    side: Side
    defense_icons: int
    defending_faction_icons: list[Faction]
    attacking_faction_icons: list[Faction]
    victory_point_value: int
    cards: list[FactionCard]
    card_text: str
    attack_tokens: int = 0
    defense_tokens: int = 0

    # p16: If this battleground gets reactivated from the other side's scoring
    # area, then defending icons are ignored.
    cancel_defending_icons: bool = False

    def card_is_playable(self, card: FactionCard) -> bool:
        # Only armies and characters can be played to battlegrounds
        # Given that the card type is right, the battleground faction needs to match
        return (
            card.card_type in [CardType.ARMY, CardType.CHARACTER]
            and card.faction
            in self.attacking_faction_icons + self.defending_faction_icons
        )

    def name(self) -> str:
        return self.title

    def attacking_cards(self) -> list[FactionCard]:
        return [
            card for card in self.cards if card.faction in self.attacking_faction_icons
        ]

    def defending_cards(self) -> list[FactionCard]:
        return [
            card for card in self.cards if card.faction in self.defending_faction_icons
        ]

    def __str__(self) -> str:
        card_string = f"{self.title} ({self.side.name})\n"

        if self.card_text != "":
            card_string += f"Card Text: {self.card_text}\n"

        card_string += f"Defense Icons: {self.defense_icons}\n"
        card_string += f"Defending Faction Icons: {[faction.name for faction in self.defending_faction_icons]}\n"
        card_string += f"Attacking Faction Icons: {[faction.name for faction in self.attacking_faction_icons]}\n"
        card_string += f"Victory Point Value: {self.victory_point_value}\n"

        # TODO: Print a summary of who's winning the battle.
        if len(self.cards) > 0:
            card_string += f"Cards:\n{'\n'.join(indent(f'{card.title} ({card.faction.name})', 2) for card in sorted(self.cards, key=lambda card: card.faction))}"

        return card_string


def make_battleground(
    title: str,
    side: Side,
    defense_icons: int,
    defending_faction_icons: list[Faction],
    attacking_faction_icons: list[Faction],
    victory_point_value: int,
    card_text: str,
) -> Battleground:
    return Battleground(
        title,
        side,
        defense_icons,
        defending_faction_icons,
        attacking_faction_icons,
        victory_point_value,
        [],
        card_text,
    )
