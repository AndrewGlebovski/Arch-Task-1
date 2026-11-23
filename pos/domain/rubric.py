from typing import Iterable
from .criterion import Criterion
from .values import CriterionId
from .errors import DomainError


class Rubric:
    def __init__(self, criteria: Iterable[Criterion] = ()):
        self._items: dict[CriterionId, Criterion] = {}
        for c in criteria:
            self.add(c)

    def add(self, criterion: Criterion) -> None:
        if criterion.id in self._items:
            raise DomainError("criterion already exists")
        if any(c.name == criterion.name for c in self._items.values()):
            raise DomainError("criterion name must be unique")
        self._items[criterion.id] = criterion

    def find(self, cid: CriterionId) -> Criterion | None:
        return self._items.get(cid)

    def all(self) -> tuple[Criterion, ...]:
        return tuple(self._items.values())

    def __len__(self) -> int:
        return len(self._items)
