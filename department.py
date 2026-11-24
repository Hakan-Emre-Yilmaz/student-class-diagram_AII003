"""Department class: a faculty department that groups its students."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from student import Student


class Department:
    """UML: Department "1" o-- "0..*" Student (aggregation)."""

    def __init__(self, code: str, name: str) -> None:
        if not code.strip() or not name.strip():
            raise ValueError("Department code and name are required.")
        self._code = code.strip()
        self._name = name.strip()
        self._students: list[Student] = []

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def students(self) -> list[Student]:
        return list(self._students)

    def register_student(self, student: Student) -> None:
        """Called by Student so both sides of the association stay in sync."""
        if student not in self._students:
            self._students.append(student)

    def top_student(self) -> Student | None:
        """Return the student with the highest GPA, or None if empty."""
        if not self._students:
            return None
        return max(self._students, key=lambda s: s.calculate_gpa())

    def __str__(self) -> str:
        return f"{self._name} [{self._code}] - {len(self._students)} student(s)"
