from dataclasses import dataclass
from wotr.agent import Agent

from wotr.deck import Deck
from wotr.faction_card import FactionCard
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
            if card is None:
                print("couldn't draw a card")
            else:
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

    def eliminate_specific(self, card: FactionCard) -> None:
        pass

    def cycle_specific(self, card: FactionCard) -> None:
        # TODO
        pass

    def draw_phase(self) -> None:
        # TODO
        pass
