"""Enrollment class: association class linking a Student to a Course."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from course import Course
    from student import Student

# Near East University letter grades -> grade points (4.0 scale)
GRADE_POINTS: dict[str, float] = {
    "AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
    "CC": 2.0, "DC": 1.5, "DD": 1.0, "FF": 0.0,
}


class Enrollment:
    """UML association class between Student and Course.

    Holds the data that belongs to the *relationship* itself:
    the semester and the letter grade.
    """

    def __init__(self, student: Student, course: Course, semester: str) -> None:
        self._student = student
        self._course = course
        self._semester = semester
        self._letter_grade: str | None = None

    @property
    def student(self) -> Student:
        return self._student

    @property
    def course(self) -> Course:
        return self._course

    @property
    def semester(self) -> str:
        return self._semester

    @property
    def letter_grade(self) -> str | None:
        return self._letter_grade

    def set_grade(self, letter: str) -> None:
        letter = letter.upper()
        if letter not in GRADE_POINTS:
            raise ValueError(f"Invalid grade '{letter}'. Use one of {list(GRADE_POINTS)}.")
        self._letter_grade = letter

    def grade_points(self) -> float | None:
        return None if self._letter_grade is None else GRADE_POINTS[self._letter_grade]

    def __str__(self) -> str:
        grade = self._letter_grade or "--"
        return f"{self._semester:<10} {self._course.code:<8} {self._course.ects} ECTS  {grade}"
