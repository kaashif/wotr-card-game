from typing import Callable
from wotr.battleground import Battleground
from wotr.enums import CardType, Faction, Side
from wotr.state import State


all_battlegrounds: list[Battleground] = []


def battleground(
    title: str,
    side: Side,
    defense_icons: int,
    defending_faction_icons: list[Faction],
    attacking_faction_icons: list[Faction],
    victory_point_value: int,
) -> Callable:
    def create_battleground_given_activate(
        activate: Callable[[Battleground, State], None]
    ) -> None:
        battleground_object = Battleground(
            side,
            defense_icons,
            defending_faction_icons,
            title,
            attacking_faction_icons,
            victory_point_value,
            [],
            activate,
        )
        all_battlegrounds.append(battleground_object)

    return create_battleground_given_activate


@battleground(
    "Helms Deep",
    side=Side.FREE,
    defense_icons=2,
    defending_faction_icons=[Faction.WIZARD, Faction.ROHAN],
    attacking_faction_icons=[Faction.ISENGARD],
    victory_point_value=2,
)
def helms_deep(self: Battleground, state: State) -> None:
    rohan_player = state.faction_to_player(Faction.ROHAN)

    # Draw 5, may play one army or character on Helms Deep
    cards = rohan_player.draw_n(5)
    playable_cards = [card for card in cards if self.card_is_playable(card)]

    if rohan_player.agent.pick_boolean():
        # TODO: no cards?
        card = rohan_player.agent.pick_no_fallback(playable_cards)
        helms_deep_location = state.get_battleground_by_name("Helms Deep")
        state.play_card(rohan_player, card, helms_deep_location)

    # Cards not played are cycled
    for card in playable_cards:
        rohan_player.cycle_pile.add_to_bottom(card)
