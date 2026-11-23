from typing import Protocol
from .evaluation import Evaluation
from .rubric import Rubric
from .values import TotalScore
from .errors import DomainError


class TotalScoreStrategy(Protocol):
    def total(self, evaluations: list[Evaluation], rubric: Rubric) -> float: ...


class WeightedSumStrategy:
    def total(self, evaluations: list[Evaluation], rubric: Rubric) -> float:
        return sum(
            ev.score.value * rubric.find(ev.criterion_id).weight.value
            for ev in evaluations
        )


class TotalScoreCalculator:
    def __init__(self, strategy: TotalScoreStrategy):
        self._strategy = strategy

    def calculate(self, evaluations: list[Evaluation], rubric: Rubric) -> TotalScore:
        for ev in evaluations:
            if rubric.find(ev.criterion_id) is None:
                raise DomainError(f"evaluation {ev.id.value} references missing criterion")
        return TotalScore(self._strategy.total(evaluations, rubric))
