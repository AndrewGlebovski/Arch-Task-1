from dataclasses import dataclass, field
from datetime import datetime, timezone
from .values import EvaluationId, StudentId, CriterionId, Score
from .criterion import Criterion
from .errors import DomainError


@dataclass
class Evaluation:
    id: EvaluationId
    student_id: StudentId
    criterion_id: CriterionId
    score: Score
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    comment: str = ""

    def change(self, criterion: Criterion, new_value: float) -> None:
        if criterion.id != self.criterion_id:
            raise DomainError("criterion mismatch")
        if not (0 <= new_value <= criterion.max_score.value):
            raise DomainError(f"score {new_value} out of range [0, {criterion.max_score.value}]")
        self.score = Score(new_value)
