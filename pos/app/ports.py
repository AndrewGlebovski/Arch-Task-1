from typing import Protocol
from .dto import TotalRow


class TotalScoreExporter(Protocol):
    def export(self, rows: list[TotalRow], path: str) -> None: ...
