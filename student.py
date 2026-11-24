"""Student class: the central class of the diagram."""

from __future__ import annotations

from typing import TYPE_CHECKING

from enrollment import Enrollment

if TYPE_CHECKING:
    from course import Course
    from department import Department


class Student:
    """UML: Student "0..*" --> "1" Department, Student "1" -- "0..*" Enrollment."""

    MAX_ECTS_PER_SEMESTER = 36  # class-level (static) attribute

    def __init__(self, student_no: str, first_name: str, last_name: str,
                 year: int, department: Department) -> None:
        if not student_no.isdigit():
            raise ValueError("Student number must contain only digits.")
        if not 1 <= year <= 6:
            raise ValueError("Year must be between 1 and 6.")
        self._student_no = student_no
        self._first_name = first_name
        self._last_name = last_name
        self._year = year
        self._department = department
        self._enrollments: list[Enrollment] = []
        department.register_student(self)

    # ---- attributes (encapsulated) ----
    @property
    def student_no(self) -> str:
        return self._student_no

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @property
    def email(self) -> str:
        """Derived attribute: built from the student number."""
        return f"{self._student_no}@std.neu.edu.tr"

    @property
    def year(self) -> int:
        return self._year

    @property
    def department(self) -> Department:
        return self._department

    @property
    def enrollments(self) -> list[Enrollment]:
        return list(self._enrollments)

    # ---- operations ----
    def ects_in(self, semester: str) -> int:
        return sum(e.course.ects for e in self._enrollments if e.semester == semester)

    def enroll(self, course: Course, semester: str) -> Enrollment:
        if any(e.course is course and e.semester == semester for e in self._enrollments):
            raise RuntimeError(f"Already enrolled in {course.code}.")
        if self.ects_in(semester) + course.ects > self.MAX_ECTS_PER_SEMESTER:
            raise RuntimeError(f"ECTS limit ({self.MAX_ECTS_PER_SEMESTER}) exceeded.")
        enrollment = Enrollment(self, course, semester)
        course.add_enrollment(enrollment)  # raises if the course is full
        self._enrollments.append(enrollment)
        return enrollment

    def drop(self, course: Course, semester: str) -> bool:
        for e in self._enrollments:
            if e.course is course and e.semester == semester:
                self._enrollments.remove(e)
                course.remove_enrollment(e)
                return True
        return False

    def calculate_gpa(self) -> float:
        """ECTS-weighted GPA over graded courses only."""
        graded = [e for e in self._enrollments if e.letter_grade is not None]
        total_ects = sum(e.course.ects for e in graded)
        if total_ects == 0:
            return 0.0
        return sum(e.grade_points() * e.course.ects for e in graded) / total_ects

    def transcript(self) -> str:
        lines = [f"{self.full_name} ({self._student_no}) - Year {self._year}",
                 f"{self._department.name}", "-" * 40]
        lines += [str(e) for e in self._enrollments] or ["No courses."]
        lines.append(f"GPA: {self.calculate_gpa():.2f}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
