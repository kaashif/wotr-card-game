from re import M
from wotr.battleground import BattlegroundDeck
from wotr.path import PathDeck
from wotr.state import State
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import ActionType, Side, PlayerCharacter

def main():
    state = State(
        shadow_scoring_area=ShadowScoringArea([], [], 0),
        free_scoring_area=FreeScoringArea([], []),
        frodo_player = Player(PlayerCharacter.FRODO),
        witch_king_player = Player(PlayerCharacter.WITCH_KING),
        aragorn_player = Player(PlayerCharacter.ARAGORN),
        saruman_player = Player(PlayerCharacter.SARUMAN),
        shadow_battleground_deck = BattlegroundDeck(Side.SHADOW),
        free_battleground_deck = BattlegroundDeck(Side.FREE),
        path_deck = PathDeck(),
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
        player.draw(7)
        
        # Choice here
        player.cycle(2)

    while True:
        # p8: The Game Round

        # Location Step
        # The starting player first activates one battleground then one path
        if state.starting_side() == Side.FREE:
            active_battleground = state.free_battleground_deck.draw()
        else:
            active_battleground = state.shadow_battleground_deck.draw()

        # May result in a choice
        active_battleground.activate()

        active_path = state.path_deck.draw_path(state.current_path)

        # May result in a choice
        active_path.activate()

        # p10: Action Step

        for player in state.player_turns():
            print(f"{player.view_string()}")

            did_action = False

            while not did_action:
                print("Choose an action type:")
                for action_type in ActionType:
                    print(f"({action_type.value}) {action_type.name}")
                chosen_action_type = ActionType(int(input("> ")))

                # TODO
                match chosen_action_type:
                    case ActionType.PLAY_CARD:
                        pass
                    case ActionType.MOVE_FROM_RESERVE:
                        pass
                    case ActionType.CYCLE:
                        pass
                    case ActionType.WINNOW:
                        if player.can_winnow():
                            player.winnow()
                            did_action = True
                    case ActionType.CARD_ACTION:
                        pass
                    case ActionType.RING_TOKEN:
                        pass
                    case ActionType.PASS:
                        if player.can_pass():
                            player.pass_turn()
                            did_action = True

                if did_action and chosen_action_type != ActionType.PASS:
                    player.unpass_turn()

            
            if all(player.passed for player in state.all_players()):
                # If all players have passed consecutively, the Action step ends
                break


        # Combat Step
        active_battleground.resolve()
        active_path.resolve()

        
        # Victory Check
        if state.is_game_over():
            state.end_game()
            break

        # Draw Step
        # FP draw 3, Shadow draws 4.
        # TODO

        # Starting player token is passed to next player in order
        state.current_path += 1
        state



if __name__ == "__main__":
    main()
