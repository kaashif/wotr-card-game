from wotr.action import Action, list_actions
from wotr.battleground import BattlegroundDeck
from wotr.path import PathDeck
from wotr.state import State
from wotr.scoring_area import FreeScoringArea, ShadowScoringArea
from wotr.player import Player
from wotr.enums import Side, PlayerCharacter

def pick_action(actions: list[Action]) -> Action:
    num_actions = len(actions)

    print("Choose an action:")

    for i in range(num_actions):
        print(f"{i}: {actions[i]}")

    while True:
        try:
            action_index = int(input(f"Enter an action index (0-{num_actions - 1})"))
            return actions[action_index]
        except Exception as e:
            print(e)

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
            state.active_battleground = state.free_battleground_deck.draw()
        else:
            state.active_battleground = state.shadow_battleground_deck.draw()

        # May result in a choice
        state.active_battleground.activate()

        state.active_path = state.path_deck.draw_path(state.current_path_number)

        # May result in a choice
        state.active_path.activate()

        # p10: Action Step

        for player in state.player_turns():
            print(f"{player.view_string()}")

            possible_actions = list_actions(state, player)
            action = pick_action(possible_actions)

            print(f"chosen action: {action}")

            action.execute()
            
            if all(player.passed for player in state.all_players()):
                # If all players have passed consecutively, the Action step ends
                break


        # Combat Step
        state.active_battleground.resolve()
        state.active_path.resolve()

        
        # Victory Check
        if state.is_game_over():
            state.end_game()
            break

        # Draw Step
        # FP draw 3, Shadow draws 4.
        # TODO

        # Starting player token is passed to next player in order
        state.current_path_number += 1
        state.game_round += 1



if __name__ == "__main__":
    main()
