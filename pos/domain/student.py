from dataclasses import dataclass
from .values import StudentId
from .errors import DomainError


@dataclass
class Student:
    id: StudentId
    full_name: str

    def __post_init__(self):
        if not self.full_name.strip():
            raise DomainError("student name must not be empty")
