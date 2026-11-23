from pos.domain.student import Student
from pos.domain.rubric import Rubric
from pos.domain.evaluation import Evaluation
from pos.domain.values import StudentId, EvaluationId


class InMemoryStudentRepository:
    def __init__(self): self._items: dict = {}
    def save(self, s): self._items[s.id] = s
    def find(self, sid): return self._items.get(sid)
    def all(self): return list(self._items.values())


class InMemoryRubricRepository:
    def __init__(self, initial: Rubric):
        self._rubric = initial
    def get(self): return self._rubric
    def save(self, r): self._rubric = r


class InMemoryEvaluationRepository:
    def __init__(self): self._items: dict = {}
    def save(self, e): self._items[e.id] = e
    def find(self, eid): return self._items.get(eid)
    def by_student(self, sid): return [e for e in self._items.values() if e.student_id == sid]
    def all(self): return list(self._items.values())
    def delete(self, eid): self._items.pop(eid, None)
