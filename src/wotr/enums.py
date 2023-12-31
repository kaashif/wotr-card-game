from enum import Enum, StrEnum, auto


class Side(StrEnum):
    SHADOW = auto()
    FREE = auto()


class PlayerCharacter(StrEnum):
    FRODO = auto()
    WITCH_KING = auto()
    ARAGORN = auto()
    SARUMAN = auto()


class Faction(StrEnum):
    DUNEDAIN = auto()
    DWARF = auto()
    ELF = auto()
    HOBBIT = auto()
    ROHAN = auto()
    WIZARD = auto()
    ISENGARD = auto()
    MONSTROUS = auto()
    MORDOR = auto()
    SOUTHRON = auto()


class CardType(StrEnum):
    ARMY = auto()
    CHARACTER = auto()
    EVENT = auto()
    ITEM = auto()


class CharacterClass(StrEnum):
    NAZGUL = auto()
    HOBBIT = auto()


class ActionType(Enum):
    PLAY_CARD = auto()
    MOVE_FROM_RESERVE = auto()
    CYCLE = auto()
    WINNOW = auto()
    CARD_ACTION = auto()
    RING_TOKEN = auto()
    PASS = auto()
