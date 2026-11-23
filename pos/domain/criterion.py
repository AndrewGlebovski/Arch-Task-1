from dataclasses import dataclass
from .values import CriterionId, MaxScore, Weight


@dataclass(frozen=True)
class Criterion:
    id: CriterionId
    name: str
    max_score: MaxScore
    weight: Weight
