from dataclasses import dataclass
from wotr.agent import Agent

from wotr.deck import Deck
from wotr.faction_card import FactionCard
from wotr.reserve import Reserve
from wotr.enums import PlayerCharacter
from wotr.cards import get_cards_for_character
from wotr.state import State

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

    def __init__(self, character: PlayerCharacter, agent: Agent) -> None:
        self.character = character
        self.hand = []
        self.draw_deck = Deck(get_cards_for_character(character))
        self.cycle_pile = Deck([])
        self.eliminated_pile = Deck([])
        self.reserve = Reserve([])
        self.agent = agent

    def draw_one(self) -> FactionCard | None:
        # p12: When you deplete your draw deck, you must immediately recycle the cycle pile.
        # This means that if we have no cards when we attempt to draw, we have no cards in any deck.
        if self.draw_deck.is_empty():
            return None

        card = self.draw_deck.draw()

        # If draw deck is depleted, recycle immediately
        if self.draw_deck.is_empty():
            self.cycle_pile.shuffle_into(self.draw_deck)

        return card

    def draw_n(self, n: int) -> list[FactionCard]:
        cards = []

        for _ in range(n):
            card = self.draw_one()
            if card is not None:
                cards.append(card)

        return cards

    def draw_n_to_hand(self, n: int) -> None:
        cards = self.draw_n(n)
        self.hand += cards

    def cycle_one(self) -> None:
        print("Choose a card to cycle")
        if len(self.hand) == 0:
            raise Exception("No cards to cycle")
        chosen_card = self.agent.pick_no_fallback(self.hand)
        self.hand.remove(chosen_card)
        self.cycle_pile.add_to_bottom(chosen_card)
        print(f"Cycled: {chosen_card.title}")
    
    def cycle(self, n: int) -> None:
        for _ in range(n):
            self.cycle_one() 

    def can_pass(self) -> bool:
        # TODO
        return True

    def pass_turn(self):
        self.passed = True
        
    def unpass_turn(self):
        self.passed = False

    def use_ring_token(self):
        if self.used_ring_token:
            raise Exception("ring token already used!")
        
        self.used_ring_token = False
        self.draw_n_to_hand(2)

    
    def can_cycle(self):
        return len(self.hand) > 0
    
    def forsake_from_draw_deck(self, state: State) -> None:
        if self.draw_deck.is_empty():
            return

        card = self.draw_deck.draw()
        
        self.eliminated_pile.add_to_bottom(card)

        # Some cards have effects when forsaken from the top of the deck
        # e.g. when eliminated, cycle instead.
        card.when_forsaken_from_top_of_deck(state)

    def forsake_from_list(self, state: State, cards: list[FactionCard]) -> None:
        if len(cards) == 0:
            raise Exception("card list is empty!")

        card = self.agent.pick_no_fallback(cards)

        # We cannot just remove card from cards. That works if cards is self.hand
        # or self.reserve.cards, but not if cards is just a list of choices not directly
        # part of the game state. We need to eliminate cards *wherever it really is*.
        self.eliminate_specific(card)

        # p11: If a character is eliminated, all items it is wielding are also eliminated.
        for item in card.items:
            self.eliminated_pile.add_to_bottom(item)

    def forsake(self, state: State) -> None:
        # p13: When forsaking you can either forsake from the top of the deck, hand, or reserve.
        # p13: You can forsake an item from its wielder.
        # Note: you cannot forsake items or characters from battlegrounds or path.
        possible_forsake_locations = []

        if not self.draw_deck.is_empty() or not self.cycle_pile.is_empty():
            possible_forsake_locations.append("draw deck")

        if len(self.hand) > 0:
            possible_forsake_locations.append("hand")   

        if len(self.reserve.cards) > 0:
            possible_forsake_locations.append("reserve")

        reserve_items = [item for card in self.reserve.cards for item in card.items]

        if len(reserve_items) > 0:
            possible_forsake_locations.append("reserve item")

        forsake_location = self.agent.pick_no_fallback(possible_forsake_locations)

        if forsake_location == "draw deck":
            self.forsake_from_draw_deck(state)
        elif forsake_location == "hand":
            self.forsake_from_list(state, self.hand)
        elif forsake_location == "reserve":
            self.forsake_from_list(state, self.reserve.cards) 
        elif forsake_location == "reserve item":
            self.forsake_from_list(state, reserve_items)

    def eliminate_specific(self, card: FactionCard) -> None:
        pass

    def cycle_specific(self, card: FactionCard) -> None:
        # TODO
        pass

    def draw_phase(self) -> None:
        # TODO
        pass

    def view_string(self, state: State) -> str:
        view = ""

        view += f"Player {self.character.name}\n"
        view += f"Hand: {self.hand}\n"
        view += f"Cycle pile: {self.cycle_pile}\n"
        view += f"Eliminated pile: {self.eliminated_pile}\n"

        view += f"Active batlegrounds: {state.active_battlegrounds}\n"
        view += f"Active path: {state.active_path}\n"

        return view