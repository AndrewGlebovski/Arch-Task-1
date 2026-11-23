import pytest
from pos.domain.errors import DomainError
from pos.domain.rubric import Rubric
from pos.domain.criterion import Criterion
from pos.domain.evaluation import Evaluation
from pos.domain.values import (
    CriterionId, MaxScore, Weight, StudentId, EvaluationId, Score,
)
from pos.domain.services import TotalScoreCalculator, WeightedSumStrategy


def _criterion(name, max_score, weight):
    return Criterion(CriterionId.new(), name, MaxScore(max_score), Weight(weight))


def _ev(sid, cid, value):
    return Evaluation(EvaluationId.new(), sid, cid, Score(value))


def test_weighted_sum():
    c1, c2 = _criterion("c1", 10, 0.4), _criterion("c2", 5, 0.6)
    rubric = Rubric([c1, c2])
    sid = StudentId.new()
    evs = [_ev(sid, c1.id, 8), _ev(sid, c2.id, 4)]

    total = TotalScoreCalculator(WeightedSumStrategy()).calculate(evs, rubric)
    assert total.value == pytest.approx(8 * 0.4 + 4 * 0.6)


def test_calculator_rejects_dangling_criterion():
    c1 = _criterion("c1", 10, 1.0)
    rubric = Rubric([c1])
    ghost = _criterion("ghost", 10, 1.0)
    evs = [_ev(StudentId.new(), ghost.id, 5)]
    with pytest.raises(DomainError):
        TotalScoreCalculator(WeightedSumStrategy()).calculate(evs, rubric)
