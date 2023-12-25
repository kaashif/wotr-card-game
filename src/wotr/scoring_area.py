from dataclasses import dataclass

from wotr.battleground import Battleground
from wotr.path import Path


@dataclass
class FreeScoringArea:
    battlegrounds: list[Battleground]
    paths: list[Path]

    def total_victory_points(self) -> int:
        # TODO
        raise NotImplementedError()


@dataclass
class ShadowScoringArea:
    battlegrounds: list[Battleground]

    # Just for tracking - shadow VPs come from corruption, NOT the VPs on the path cards
    paths: list[Path]

    corruption: int

    def total_victory_points(self) -> int:
        # TODO
        raise NotImplementedError()


def make_free_scoring_area() -> FreeScoringArea:
    return FreeScoringArea([], [])


def make_shadow_scoring_area() -> ShadowScoringArea:
    return ShadowScoringArea([], [], 0)
