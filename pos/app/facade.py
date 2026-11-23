from .dto import StudentView, CriterionView, EvaluationView, TotalRow
from .ports import TotalScoreExporter
from pos.domain.student import Student
from pos.domain.criterion import Criterion
from pos.domain.evaluation import Evaluation
from pos.domain.factories import EvaluationFactory
from pos.domain.services import TotalScoreCalculator
from pos.domain.repos import (
    StudentRepository, RubricRepository, EvaluationRepository,
)
from pos.domain.values import (
    StudentId, CriterionId, EvaluationId, MaxScore, Weight,
)
from pos.domain.errors import DomainError


class AppFacade:
    def __init__(
        self,
        students: StudentRepository,
        rubric: RubricRepository,
        evaluations: EvaluationRepository,
        factory: EvaluationFactory,
        calculator: TotalScoreCalculator,
        exporter: TotalScoreExporter,
    ):
        self._students = students
        self._rubric = rubric
        self._evaluations = evaluations
        self._factory = factory
        self._calculator = calculator
        self._exporter = exporter

    def add_student(self, full_name: str) -> str:
        s = Student(StudentId.new(), full_name)
        self._students.save(s)
        return str(s.id.value)

    def list_students(self) -> list[StudentView]:
        return [StudentView(str(s.id.value), s.full_name) for s in self._students.all()]

    def add_criterion(self, name: str, max_score: float, weight: float) -> str:
        c = Criterion(CriterionId.new(), name, MaxScore(max_score), Weight(weight))
        rubric = self._rubric.get()
        rubric.add(c)
        self._rubric.save(rubric)
        return str(c.id.value)

    def list_criteria(self) -> list[CriterionView]:
        return [
            CriterionView(str(c.id.value), c.name, c.max_score.value, c.weight.value)
            for c in self._rubric.get().all()
        ]

    def evaluate(self, student_id: str, criterion_id: str, value: float, comment: str = "") -> str:
        sid = StudentId(self._parse_uuid(student_id))
        cid = CriterionId(self._parse_uuid(criterion_id))
        if self._students.find(sid) is None:
            raise DomainError("student not found")
        ev = self._factory.create(sid, cid, value, comment)
        self._evaluations.save(ev)
        return str(ev.id.value)

    def list_evaluations(self, student_id: str) -> list[EvaluationView]:
        sid = StudentId(self._parse_uuid(student_id))
        rubric = self._rubric.get()
        rows = []
        for ev in self._evaluations.by_student(sid):
            crit = rubric.find(ev.criterion_id)
            rows.append(EvaluationView(
                id=str(ev.id.value),
                student_id=str(ev.student_id.value),
                criterion_id=str(ev.criterion_id.value),
                criterion_name=crit.name if crit else "<missing>",
                score=ev.score.value,
                comment=ev.comment,
            ))
        return rows

    def change(self, evaluation_id: str, new_value: float) -> None:
        ev = self._evaluations.find(EvaluationId(self._parse_uuid(evaluation_id)))
        if ev is None:
            raise DomainError("evaluation not found")
        crit = self._rubric.get().find(ev.criterion_id)
        if crit is None:
            raise DomainError("criterion of this evaluation is missing")
        ev.change(crit, new_value)
        self._evaluations.save(ev)

    def cancel(self, evaluation_id: str) -> None:
        self._evaluations.delete(EvaluationId(self._parse_uuid(evaluation_id)))

    def total(self, student_id: str) -> TotalRow:
        sid = StudentId(self._parse_uuid(student_id))
        student = self._students.find(sid)
        if student is None:
            raise DomainError("student not found")
        rubric = self._rubric.get()
        evs = self._evaluations.by_student(sid)
        total = self._calculator.calculate(evs, rubric)
        return TotalRow(str(sid.value), student.full_name, total.value)

    def export_totals(self, path: str) -> None:
        rows = [self.total(str(s.id.value)) for s in self._students.all()]
        self._exporter.export(rows, path)

    @staticmethod
    def _parse_uuid(s: str):
        from uuid import UUID
        try:
            return UUID(s)
        except ValueError:
            raise DomainError(f"invalid id: {s}")
