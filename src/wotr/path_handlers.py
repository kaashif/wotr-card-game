from wotr.enums import PlayerCharacter
from wotr.event_handler import EventType, register
from wotr.game import Game


@register(EventType.ACTIVATE, "Bag End")
def activate_bag_end(game: Game) -> None:
    game.character_to_player(PlayerCharacter.FRODO).draw_n_to_hand(2)
