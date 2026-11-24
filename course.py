"""Course class: a course with a limited capacity."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enrollment import Enrollment


class Course:
    """UML: Course "1" -- "0..*" Enrollment."""

    def __init__(self, code: str, title: str, ects: int, capacity: int = 30) -> None:
        if ects <= 0:
            raise ValueError("ECTS must be positive.")
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self._code = code
        self._title = title
        self._ects = ects
        self._capacity = capacity
        self._enrollments: list[Enrollment] = []

    @property
    def code(self) -> str:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    @property
    def ects(self) -> int:
        return self._ects

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def enrollments(self) -> list[Enrollment]:
        return list(self._enrollments)

    def is_full(self) -> bool:
        return len(self._enrollments) >= self._capacity

    def add_enrollment(self, enrollment: Enrollment) -> None:
        if self.is_full():
            raise RuntimeError(f"{self._code} is full ({self._capacity} seats).")
        self._enrollments.append(enrollment)

    def remove_enrollment(self, enrollment: Enrollment) -> None:
        if enrollment in self._enrollments:
            self._enrollments.remove(enrollment)

    def class_list(self) -> list[str]:
        return [e.student.full_name for e in self._enrollments]

    def __str__(self) -> str:
        return (f"{self._code} - {self._title} ({self._ects} ECTS, "
                f"{len(self._enrollments)}/{self._capacity} seats)")
