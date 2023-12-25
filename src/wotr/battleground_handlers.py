from wotr.enums import Faction
from wotr.event_handler import EventType, register
from wotr.game import Game


@register(
    EventType.ACTIVATE,
    "Helms Deep",
)
def activate_helms_deep(game: Game) -> None:
    helms_deep = game.get_battleground_by_name("Helms Deep")
    rohan_player = game.faction_to_player(Faction.ROHAN)

    # Draw 5, may play one army or character on Helms Deep
    cards = rohan_player.draw_n(5)
    playable_cards = [card for card in cards if helms_deep.card_is_playable(card)]

    if rohan_player.agent.pick_boolean():
        # TODO: no cards?
        card = rohan_player.agent.pick_no_fallback(playable_cards)
        game.play_card(rohan_player, card, helms_deep)

    # Cards not played are cycled
    for card in playable_cards:
        rohan_player.cycle_pile.add_to_bottom(card)
