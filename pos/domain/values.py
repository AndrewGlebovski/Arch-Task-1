from dataclasses import dataclass
from uuid import UUID, uuid4
from .errors import DomainError


@dataclass(frozen=True)
class StudentId:
    value: UUID
    @classmethod
    def new(cls) -> "StudentId":
        return cls(uuid4())


@dataclass(frozen=True)
class CriterionId:
    value: UUID
    @classmethod
    def new(cls) -> "CriterionId":
        return cls(uuid4())


@dataclass(frozen=True)
class EvaluationId:
    value: UUID
    @classmethod
    def new(cls) -> "EvaluationId":
        return cls(uuid4())


@dataclass(frozen=True)
class Score:
    value: float
    def __post_init__(self):
        if self.value < 0:
            raise DomainError("score must be >= 0")


@dataclass(frozen=True)
class MaxScore:
    value: float
    def __post_init__(self):
        if self.value <= 0:
            raise DomainError("max_score must be > 0")


@dataclass(frozen=True)
class Weight:
    value: float
    def __post_init__(self):
        if not (0 < self.value <= 1):
            raise DomainError("weight must be in (0, 1]")


@dataclass(frozen=True)
class TotalScore:
    value: float
