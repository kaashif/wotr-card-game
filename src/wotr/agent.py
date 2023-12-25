from abc import ABC, abstractmethod
import random
from typing import TypeVar, cast
from wotr.util import indent

T = TypeVar("T")


class Agent(ABC):
    @abstractmethod
    def pick_with_fallback(self, choices: list[T], fallback: str = "back") -> T | None:
        raise NotImplementedError()

    @abstractmethod
    def pick_no_fallback(self, choices: list[T]) -> T:
        raise NotImplementedError()

    def pick_boolean(self) -> bool:
        return self.pick_no_fallback([True, False])


class HumanAgent(Agent):
    def pick_from_list(self, choices: list[T]) -> T | None:
        if len(choices) == 0:
            print("choices empty")
            return None

        for i in range(len(choices)):
            print(f"{i}:\n{indent(str(choices[i]), 2)}\n")

        while True:
            try:
                choice = input(f"Make a choice from 0-{len(choices)-1}: ")
                chosen_index = int(choice)

                if 0 <= chosen_index < len(choices):
                    break
                else:
                    print("choice not in range!")

            except Exception as e:
                print(e)

        print(f"chose: {choices[chosen_index]}")

        return choices[chosen_index]

    def pick_with_fallback(self, choices: list[T], fallback: str = "back") -> T | None:
        choices_and_back = choices + [fallback]
        choice = self.pick_from_list(choices_and_back)

        if choice == fallback:
            return None

        return cast(T, choice)

    def pick_no_fallback(self, choices: list[T]) -> T:
        choice = self.pick_from_list(choices)
        assert choice is not None
        return choice


class RandomAgent(Agent):
    def pick_with_fallback(self, choices: list[T], fallback: str = "back") -> T | None:
        if len(choices) == 0:
            return None

        return random.choice(choices)

    def pick_no_fallback(self, choices: list[T]) -> T:
        return random.choice(choices)
