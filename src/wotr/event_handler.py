from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, TypeAlias, TypeVar


class EventType(Enum):
    ACTIVATE = auto()


@dataclass
class Event:
    event_type: EventType
    subject_name: str

    def __hash__(self) -> int:
        return hash((self.event_type, self.subject_name))


T = TypeVar("T")
EventHandler: TypeAlias = Callable[[T], None]

event_to_handler: dict[Event, EventHandler] = {}


def register(
    event_type: EventType, subject_name: str
) -> Callable[[EventHandler], EventHandler]:
    def register_and_return_handler(handler: EventHandler) -> EventHandler:
        event_to_handler[Event(event_type, subject_name)] = handler
        return handler

    return register_and_return_handler
