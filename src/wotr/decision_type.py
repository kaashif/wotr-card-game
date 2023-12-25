from enum import Enum, auto


class DecisionType(Enum):
    WHICH_CARD_TO_PLAY = auto()
    WHERE_TO_PLAY_CARD = auto()
    WHICH_CARD_TO_CYCLE = auto()
    WHERE_TO_FORSAKE_FROM = auto()
    WHICH_ACTION_TO_DO = auto()
    WHICH_CARD_TO_MOVE_FROM_RESERVE = auto()
    WHERE_TO_MOVE_CARD_FROM_RESERVE = auto()
    WHICH_CARD_TO_ELIMINATE = auto()
    WHICH_CARD_ACTION_TO_DO = auto()


def get_nice_string(decision_type: DecisionType) -> str:
    map = {
        DecisionType.WHICH_CARD_TO_PLAY: "Which card to play",
        DecisionType.WHERE_TO_PLAY_CARD: "Where to play card",
        DecisionType.WHICH_CARD_TO_CYCLE: "Which card to cycle",
        DecisionType.WHERE_TO_FORSAKE_FROM: "Where to forsake from",
        DecisionType.WHICH_ACTION_TO_DO: "Which action to do",
        DecisionType.WHICH_CARD_TO_MOVE_FROM_RESERVE: "Which card to move from reserve",
        DecisionType.WHERE_TO_MOVE_CARD_FROM_RESERVE: "Where to move card from reserve",
        DecisionType.WHICH_CARD_TO_ELIMINATE: "Which card to eliminate",
        DecisionType.WHICH_CARD_ACTION_TO_DO: "Which card action to do",
    }

    return map[decision_type]
