from dataclasses import dataclass

@dataclass
class Player:
    hand: list[FactionCard]
    draw_deck: Deck
    cycle_pile: Deck
    eliminated_pile: Deck
    reserve: Reserve
    