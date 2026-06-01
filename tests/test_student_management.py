import tempfile
import unittest
from pathlib import Path

from student_management import Student, StudentManagementSystem


class StudentManagementSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "students.json"
        self.system = StudentManagementSystem(str(self.file_path))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_search_student(self) -> None:
        added = self.system.add_student(Student(student_id="1", name="Alice", age=20, course="CS"))
        self.assertTrue(added)

        student = self.system.search_student("1")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Alice")

    def test_update_student(self) -> None:
        self.system.add_student(Student(student_id="2", name="Bob", age=21, course="Math"))

        updated = self.system.update_student("2", name="Bobby", age=22)
        self.assertTrue(updated)

        student = self.system.search_student("2")
        self.assertEqual(student.name, "Bobby")
        self.assertEqual(student.age, 22)

    def test_delete_student(self) -> None:
        self.system.add_student(Student(student_id="3", name="Cara", age=19, course="Physics"))

        deleted = self.system.delete_student("3")
        self.assertTrue(deleted)
        self.assertIsNone(self.system.search_student("3"))

    def test_duplicate_student_id_is_rejected(self) -> None:
        self.system.add_student(Student(student_id="4", name="Dan", age=23, course="Biology"))

        added = self.system.add_student(Student(student_id="4", name="Daniel", age=24, course="Chemistry"))
        self.assertFalse(added)

    def test_invalid_json_file_is_handled(self) -> None:
        self.file_path.write_text("{", encoding="utf-8")
        self.assertIsNone(self.system.search_student("1"))


if __name__ == "__main__":
    unittest.main()
