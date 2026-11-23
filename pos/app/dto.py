from dataclasses import dataclass


@dataclass(frozen=True)
class StudentView:
    id: str
    full_name: str


@dataclass(frozen=True)
class CriterionView:
    id: str
    name: str
    max_score: float
    weight: float


@dataclass(frozen=True)
class EvaluationView:
    id: str
    student_id: str
    criterion_id: str
    criterion_name: str
    score: float
    comment: str


@dataclass(frozen=True)
class TotalRow:
    student_id: str
    student_name: str
    total: float
