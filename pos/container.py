from pos.infra.memory_repos import (
    InMemoryStudentRepository, InMemoryRubricRepository, InMemoryEvaluationRepository,
)
from pos.infra.csv_exporter import CsvTotalScoreExporter
from pos.domain.factories import EvaluationFactory
from pos.domain.services import TotalScoreCalculator, WeightedSumStrategy
from pos.domain.rubric import Rubric
from pos.app.facade import AppFacade


class Container:
    def __init__(self):
        self.students = InMemoryStudentRepository()
        self.rubric = InMemoryRubricRepository(Rubric())
        self.evaluations = InMemoryEvaluationRepository()

        self.factory = EvaluationFactory(self.rubric)
        self.calculator = TotalScoreCalculator(WeightedSumStrategy())
        self.exporter = CsvTotalScoreExporter()

        self.facade = AppFacade(
            self.students, self.rubric, self.evaluations,
            self.factory, self.calculator, self.exporter,
        )
