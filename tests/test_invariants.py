import pytest
from pos.domain.errors import DomainError
from pos.domain.rubric import Rubric
from pos.domain.criterion import Criterion
from pos.domain.values import CriterionId, MaxScore, Weight, StudentId
from pos.domain.factories import EvaluationFactory


class FakeRubricRepo:
    def __init__(self, rubric: Rubric): self._r = rubric
    def get(self): return self._r
    def save(self, rubric: Rubric): self._r = rubric


def _factory_with_criterion(max_score=10.0):
    cid = CriterionId.new()
    crit = Criterion(cid, "Test", MaxScore(max_score), Weight(0.5))
    return EvaluationFactory(FakeRubricRepo(Rubric([crit]))), cid


def test_score_out_of_range_rejected():
    factory, cid = _factory_with_criterion(10)
    with pytest.raises(DomainError):
        factory.create(StudentId.new(), cid, 12)


def test_negative_score_rejected():
    factory, cid = _factory_with_criterion(10)
    with pytest.raises(DomainError):
        factory.create(StudentId.new(), cid, -1)


def test_unknown_criterion_rejected():
    factory, _ = _factory_with_criterion(10)
    with pytest.raises(DomainError):
        factory.create(StudentId.new(), CriterionId.new(), 5)
