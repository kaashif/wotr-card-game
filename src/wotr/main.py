from wotr.agent import HumanAgent
from wotr.battleground import BattlegroundDeck
from wotr.path import PathDeck
from wotr.state import State
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import Side, PlayerCharacter, ActionType


def main():
    # TODO: random number generator must be seeded at the start so objects behave deterministically
    state = State(
        shadow_scoring_area=ShadowScoringArea([], [], 0),
        free_scoring_area=FreeScoringArea([], []),
        frodo_player=Player(PlayerCharacter.FRODO, HumanAgent()),
        witch_king_player=Player(PlayerCharacter.WITCH_KING, HumanAgent()),
        aragorn_player=Player(PlayerCharacter.ARAGORN, HumanAgent()),
        saruman_player=Player(PlayerCharacter.SARUMAN, HumanAgent()),
        shadow_battleground_deck=BattlegroundDeck(Side.SHADOW),
        free_battleground_deck=BattlegroundDeck(Side.FREE),
        path_deck=PathDeck(),
        active_battlegrounds=[],
    )

    # 1. Select a scenario
    # Always trilogy scenario
    # TODO: Support other scenarios

    # 2. Prepare the players' decks

    for player in state.all_players():
        player.draw_deck.shuffle()

    # 3. Arrange the battleground and path decks.

    state.shadow_battleground_deck.shuffle()
    state.free_battleground_deck.shuffle()

    # Path deck is already arranged

    # 4. Draw cards and cycle
    for player in state.all_players():
        print("Each player draws 7 cards and cycles two.")
        player.draw_n_to_hand(7)

        # Choice here
        player.cycle(2)

    while True:
        # p8: The Game Round

        # Location Step
        # The starting player first activates one battleground then one path
        if state.get_side_for_round() == Side.FREE:
            state.active_battlegrounds.append(state.free_battleground_deck.draw())
        else:
            state.active_battlegrounds.append(state.shadow_battleground_deck.draw())

        # May result in a choice
        state.active_battlegrounds[0].activate(state)

        state.active_path = state.path_deck.draw_path(state.current_path_number)

        # May result in a choice
        state.active_path.activate(state)

        # p10: Action Step

        for player in state.player_turns():
            print(f"{player.view_string(state)}")

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
                            list(state.get_playable_locations(player, card))
                        )

                        if place_to_play is None:
                            continue

                        state.play_card(player, card, place_to_play)

                        if player.can_cycle():
                            player.cycle(1)
                        else:
                            player.forsake(state)

                        did_action = True

                    case ActionType.MOVE_FROM_RESERVE:
                        print("choose a card in reserve:")
                        card = player.agent.pick_with_fallback(player.reserve.cards)

                        if card is None:
                            continue

                        print("choose a place to move it:")
                        place_to_move = player.agent.pick_with_fallback(
                            list(state.get_playable_locations(player, card))
                        )

                        if place_to_move is None:
                            continue

                        state.move_card_from_reserve(player, card, place_to_move)
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
                            state.cards_with_doable_actions_for_player(player)
                        )

                        if card is None:
                            continue

                        state.perform_card_action(card)
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

            if all(player.passed for player in state.all_players()):
                # If all players have passed consecutively, the Action step ends
                print("action phase is over")
                break

        # Combat Step
        print("resolving combat")

        state.resolve_battlegrounds()
        state.resolve_active_path()

        # Victory Check
        print("checking for victory")
        if state.is_game_over():
            state.end_game()
            break

        # Draw Step
        # FP draw 3, Shadow draws 4.
        print("executing draw phase")
        for player in state.all_players():
            player.draw_phase()

        # Starting player token is passed to next player in order
        state.current_path_number += 1
        state.game_round += 1

        # TODO: Verify invariants - all cards still exist somewhere


if __name__ == "__main__":
    main()
