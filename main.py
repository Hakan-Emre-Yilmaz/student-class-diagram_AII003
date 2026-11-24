"""Demo: creates objects from the class diagram and shows their relationships."""

from course import Course
from department import Department
from student import Student


def header(text: str) -> None:
    print(f"\n--- {text} ---")


def main() -> None:
    dept = Department("COM", "Computer Engineering")

    ict = Course("AII003", "Information and Communication Technologies", 6, capacity=2)
    data_structures = Course("AII201", "Data Structures", 6)
    operating_systems = Course("ECC302", "Operating Systems", 6)

    hakan = Student("20221703", "Hakan Emre", "Yilmaz", 4, dept)
    ayse = Student("20231001", "Ayse", "Demir", 3, dept)
    mehmet = Student("20231002", "Mehmet", "Kaya", 2, dept)

    header("Department")
    print(dept)
    for s in dept.students:
        print(" ", s)

    header("Enrollment")
    term = "Fall 2026"
    r1 = hakan.enroll(ict, term)
    r2 = hakan.enroll(data_structures, term)
    r3 = hakan.enroll(operating_systems, term)
    a1 = ayse.enroll(ict, term)
    print(ict)
    print("Class list:", ", ".join(ict.class_list()))

    # Constraint check: AII003 has only 2 seats
    try:
        mehmet.enroll(ict, term)
    except RuntimeError as err:
        print("Mehmet could not enroll:", err)

    header("Grading")
    r1.set_grade("AA")
    r2.set_grade("BA")
    r3.set_grade("CB")
    a1.set_grade("BB")
    print(hakan.transcript())

    header("Drop a course")
    hakan.drop(operating_systems, term)
    print(hakan.transcript())

    header("Top student")
    best = dept.top_student()
    print(f"{best.full_name} - GPA {best.calculate_gpa():.2f}")


if __name__ == "__main__":
    main()
