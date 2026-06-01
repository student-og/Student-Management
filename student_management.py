import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    course: str


class StudentManagementSystem:
    def __init__(self, file_path: str = "students.json") -> None:
        self.file_path = Path(file_path)

    def _load_students(self) -> list[Student]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Student(**student) for student in data]

    def _save_students(self, students: list[Student]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([asdict(student) for student in students], file, indent=2)

    def add_student(self, student: Student) -> bool:
        students = self._load_students()
        if any(existing.student_id == student.student_id for existing in students):
            return False

        students.append(student)
        self._save_students(students)
        return True

    def update_student(self, student_id: str, *, name: Optional[str] = None, age: Optional[int] = None, course: Optional[str] = None) -> bool:
        students = self._load_students()
        for student in students:
            if student.student_id == student_id:
                if name is not None:
                    student.name = name
                if age is not None:
                    student.age = age
                if course is not None:
                    student.course = course
                self._save_students(students)
                return True
        return False

    def search_student(self, student_id: str) -> Optional[Student]:
        students = self._load_students()
        for student in students:
            if student.student_id == student_id:
                return student
        return None

    def delete_student(self, student_id: str) -> bool:
        students = self._load_students()
        remaining = [student for student in students if student.student_id != student_id]

        if len(remaining) == len(students):
            return False

        self._save_students(remaining)
        return True


def _print_student(student: Student) -> None:
    print(f"ID: {student.student_id}")
    print(f"Name: {student.name}")
    print(f"Age: {student.age}")
    print(f"Course: {student.course}")


def run_menu() -> None:
    system = StudentManagementSystem()

    while True:
        print("\nStudent Management System")
        print("1. Add student")
        print("2. Update student")
        print("3. Search student")
        print("4. Delete student")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            name = input("Enter name: ").strip()
            age = int(input("Enter age: ").strip())
            course = input("Enter course: ").strip()
            added = system.add_student(Student(student_id=student_id, name=name, age=age, course=course))
            print("Student added." if added else "Student ID already exists.")
        elif choice == "2":
            student_id = input("Enter student ID to update: ").strip()
            name = input("Enter new name (leave blank to keep): ").strip() or None
            age_input = input("Enter new age (leave blank to keep): ").strip()
            age = int(age_input) if age_input else None
            course = input("Enter new course (leave blank to keep): ").strip() or None
            updated = system.update_student(student_id, name=name, age=age, course=course)
            print("Student updated." if updated else "Student not found.")
        elif choice == "3":
            student_id = input("Enter student ID to search: ").strip()
            student = system.search_student(student_id)
            if student:
                _print_student(student)
            else:
                print("Student not found.")
        elif choice == "4":
            student_id = input("Enter student ID to delete: ").strip()
            deleted = system.delete_student(student_id)
            print("Student deleted." if deleted else "Student not found.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    run_menu()
