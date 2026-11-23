import csv
from pos.app.dto import TotalRow


class CsvTotalScoreExporter:
    def export(self, rows: list[TotalRow], path: str) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["student_id", "student_name", "total"])
            for r in rows:
                w.writerow([r.student_id, r.student_name, f"{r.total:.2f}"])
