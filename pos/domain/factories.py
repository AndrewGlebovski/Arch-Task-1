from .evaluation import Evaluation
from .criterion import Criterion
from .rubric import Rubric
from .repos import RubricRepository
from .values import EvaluationId, StudentId, CriterionId, Score
from .errors import DomainError


class EvaluationFactory:
    def __init__(self, rubric_repo: RubricRepository):
        self._rubric_repo = rubric_repo

    def create(
        self,
        student_id: StudentId,
        criterion_id: CriterionId,
        value: float,
        comment: str = "",
    ) -> Evaluation:
        rubric: Rubric = self._rubric_repo.get()
        criterion = rubric.find(criterion_id)
        if criterion is None:
            raise DomainError("evaluation references unknown criterion")
        if not (0 <= value <= criterion.max_score.value):
            raise DomainError(f"score {value} out of range [0, {criterion.max_score.value}]")
        return Evaluation(
            id=EvaluationId.new(),
            student_id=student_id,
            criterion_id=criterion_id,
            score=Score(value),
            comment=comment,
        )
