# These are imported for the side effect of registering event handlers.
import wotr.battleground_handlers
import wotr.path_handlers

from wotr.agent import HumanAgent
from wotr.battleground_deck import BattlegroundDeck, get_battlegrounds_for_side
from wotr.path_deck import PathDeck, all_paths
from wotr.game import Game
from wotr.scoring_area import make_free_scoring_area, make_shadow_scoring_area
from wotr.player import Player
from wotr.enums import Side, PlayerCharacter, ActionType
from wotr.event_handler import Event, EventType, event_to_handler


def main():
    # TODO: random number generator must be seeded at the start so objects behave deterministically
    game = Game(
        shadow_scoring_area=make_shadow_scoring_area(),
        free_scoring_area=make_free_scoring_area(),
        frodo_player=Player(PlayerCharacter.FRODO, HumanAgent()),
        witch_king_player=Player(PlayerCharacter.WITCH_KING, HumanAgent()),
        aragorn_player=Player(PlayerCharacter.ARAGORN, HumanAgent()),
        saruman_player=Player(PlayerCharacter.SARUMAN, HumanAgent()),
        shadow_battleground_deck=BattlegroundDeck(
            get_battlegrounds_for_side(Side.SHADOW)
        ),
        free_battleground_deck=BattlegroundDeck(get_battlegrounds_for_side(Side.FREE)),
        path_deck=PathDeck(all_paths),
        active_battlegrounds=[],
        event_to_handler=event_to_handler,
    )

    # 1. Select a scenario
    # Always trilogy scenario
    # TODO: Support other scenarios

    # 2. Prepare the players' decks

    for player in game.all_players():
        player.draw_deck.shuffle()

    # 3. Arrange the battleground and path decks.

    game.shadow_battleground_deck.shuffle()
    game.free_battleground_deck.shuffle()

    # Path deck is already arranged

    # 4. Draw cards and cycle
    for player in game.all_players():
        print("Each player draws 7 cards and cycles two.")
        player.draw_n_to_hand(7)

        # Choice here
        player.cycle(2)

    while True:
        # p8: The Game Round

        # Location Step
        # The starting player first activates one battleground then one path
        if game.get_side_for_round() == Side.FREE:
            game.active_battlegrounds.append(game.free_battleground_deck.draw())
        else:
            game.active_battlegrounds.append(game.shadow_battleground_deck.draw())

        # May result in a choice
        game.trigger_event(EventType.ACTIVATE, game.active_battlegrounds[0])

        game.active_path = game.path_deck.draw_path(game.current_path_number)

        # May result in a choice
        game.trigger_event(EventType.ACTIVATE, game.active_path)

        # p10: Action Step

        for player in game.player_turns():
            print(f"{game.get_player_view(player)}")

            did_action = False

            while not did_action:
                action_type = player.agent.pick_no_fallback(list(ActionType))

                if action_type is None:
                    print("you have to pick an action")
                    continue

                match action_type:
                    case ActionType.PLAY_CARD:
                        print("choose a card to play:")
                        card = player.agent.pick_with_fallback(player.hand)

                        if card is None:
                            continue

                        print("choose a place to play it:")
                        place_to_play = player.agent.pick_with_fallback(
                            list(game.get_playable_locations(player, card))
                        )

                        if place_to_play is None:
                            continue

                        game.play_card(player, card, place_to_play)

                        if player.can_cycle():
                            player.cycle(1)
                        else:
                            game.forsake(player)

                        did_action = True

                    case ActionType.MOVE_FROM_RESERVE:
                        print("choose a card in reserve:")
                        card = player.agent.pick_with_fallback(player.reserve.cards)

                        if card is None:
                            continue

                        print("choose a place to move it:")
                        place_to_move = player.agent.pick_with_fallback(
                            list(game.get_playable_locations(player, card))
                        )

                        if place_to_move is None:
                            continue

                        game.move_card_from_reserve(player, card, place_to_move)
                        did_action = True

                    case ActionType.CYCLE:
                        print("choose a card to cycle:")
                        card = player.agent.pick_with_fallback(player.hand)

                        if card is None:
                            continue

                        player.cycle_specific(card)
                        did_action = True

                    case ActionType.WINNOW:
                        # p13: If you don't have two cards in hand, you can't winnow.
                        if len(player.hand) < 2:
                            print("you don't have enough cards in hand to winnow!")
                            continue

                        print("choose the first card to eliminate:")
                        card1 = player.agent.pick_with_fallback(player.hand)

                        if card1 is None:
                            continue

                        print("choose the second card to eliminate:")
                        card2 = player.agent.pick_with_fallback(player.hand)

                        if card2 is None:
                            continue

                        player.eliminate_specific(card1)
                        player.eliminate_specific(card2)

                        player.draw_n_to_hand(1)
                        did_action = True

                    case ActionType.CARD_ACTION:
                        print("choose a card with an action:")
                        card = player.agent.pick_with_fallback(
                            game.cards_with_doable_actions_for_player(player)
                        )

                        if card is None:
                            continue

                        game.perform_card_action(card)
                        did_action = True

                    case ActionType.RING_TOKEN:
                        if player.used_ring_token is False:
                            player.use_ring_token()
                            did_action = True
                        else:
                            print("you already used your ring token!")

                    case ActionType.PASS:
                        if player.can_pass():
                            player.pass_turn()
                            did_action = True
                        else:
                            print("you can't pass!")

            if all(player.passed for player in game.all_players()):
                # If all players have passed consecutively, the Action step ends
                print("action phase is over")
                break

        # Combat Step
        print("resolving combat")

        game.resolve_battlegrounds()
        game.resolve_active_path()

        # Victory Check
        print("checking for victory")
        if game.is_game_over():
            game.end_game()
            break

        # Draw Step
        # FP draw 3, Shadow draws 4.
        print("executing draw phase")
        for player in game.all_players():
            player.draw_phase()

        # Starting player token is passed to next player in order
        game.current_path_number += 1
        game.game_round += 1

        # TODO: Verify invariants - all cards still exist somewhere


if __name__ == "__main__":
    main()
