from dataclasses import dataclass
from re import S

from wotr.deck import Deck
from wotr.faction_card import FactionCard, choose_faction_card
from wotr.reserve import Reserve
from wotr.enums import PlayerCharacter
from wotr.cards import get_cards_for_character

@dataclass
class Player:
    hand: list[FactionCard]
    draw_deck: Deck
    cycle_pile: Deck
    eliminated_pile: Deck
    reserve: Reserve
    character: PlayerCharacter
    used_ring_token: bool = False
    passed: bool = False

    def __init__(self, character: PlayerCharacter):
        self.character = character
        self.hand = []
        self.draw_deck = Deck(get_cards_for_character(character))
        self.cycle_pile = Deck([])
        self.eliminated_pile = Deck([])
        self.reserve = Reserve([])

    def draw_one(self) -> None:
        # p12: When you deplete your draw deck, you must immediately recycle the cycle pile.
        # This means that if we have no cards when we attempt to draw, we have no cards in any deck.
        if self.draw_deck.is_empty():
            return

        self.hand.append(self.draw_deck.draw())

        # If draw deck is depleted, recycle immediately
        if self.draw_deck.is_empty():
            self.cycle_pile.shuffle_into(self.draw_deck)


    def draw(self, n: int) -> None:
        for _ in range(n):
            self.draw_one()

    def cycle_one(self) -> None:
        print("Choose a card to cycle")
        chosen_card = choose_faction_card(self.hand)
        self.hand = [card for card in self.hand if card is not chosen_card]
        self.cycle_pile.add_to_bottom(chosen_card)
        print(f"Cycled: {chosen_card.title}")
    
    def cycle(self, n: int) -> None:
        for _ in range(n):
            self.cycle_one() 

    def winnow(self):
        # TODO
        pass

    def can_pass(self) -> bool:
        # TODO
        return True

    def view_string(self):
        print(f"Hand: {self.hand}")
        # TODO: print other relevant information

    def pass_turn(self):
        self.passed = True
        
    def unpass_turn(self):
        self.passed = False

    def use_ring_token(self):
        if self.used_ring_token:
            raise Exception("ring token already used!")
        
        self.used_ring_token = False
        self.draw(2)