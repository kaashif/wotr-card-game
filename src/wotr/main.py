from wotr.battleground import Battleground
from wotr.path import Path

def main():
    # Setup
    shadow_scoring_area = ShadowScoringArea()
    free_scoring_area = FreeScoringArea()

    # 1. Select a scenario
    # Always trilogy scenario

    # 2. Prepare the players' decks
    frodo_player = Player(FRODO)
    witch_king_player = Player(WITCH_KING)
    aragorn_player = Player(ARAGORN)
    saruman_player = Player(SARUMAN)

    players = [frodo_player, witch_king_player, aragorn_player, saruman_player]

    for player in players:
        player.draw_deck.shuffle()
    
    
    # 3. Arrange the battleground and path decks.
    shadow_battleground_deck = BattlegroundDeck(SHADOW)
    free_battleground_deck = BattlegroundDeck(FREE)
    
    shadow_battleground_deck.shuffle()
    free_battleground_deck.shuffle()
    
    path_deck = PathDeck()

    # 4. Draw cards and cycle
    for player in players:
        player.draw(7)
        player.cycle(2)
    
    
if __name__ == "__main__":
    main()