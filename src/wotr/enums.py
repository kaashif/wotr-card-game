from enum import StrEnum, auto

class Side(Enum):
    SHADOW = auto()
    FREE = auto()

class PlayerCharacter(StrEnum):
    FRODO = auto()
    WITCH_KING = auto()
    ARAGORN = auto()
    SARUMAN = auto()