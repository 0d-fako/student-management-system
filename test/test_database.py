
import unittest
import bcrypt
from app.database import DatabaseManager
from app.user import Student, Instructor
from app.course import Course


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager("test_data")
        self.student = Student("student@example.com", bcrypt.hashpw(b"password", bcrypt.gensalt()).decode(), "John", "Doe")
        self.instructor = Instructor("instructor@example.com", bcrypt.hashpw(b"password", bcrypt.gensalt()).decode(), "Jane", "Smith")
        self.course = Course("CS101", "Introduction to Computer Science", self.instructor)
        self.course.add_student(self.student)
        self.course.set_grade(self.student, "A")

    def tearDown(self):
        open(self.db.users_file, "w").close()
        open(self.db.courses_file, "w").close()

    def test_save_and_load_users(self):
        self.db.save_users([self.student, self.instructor])

        loaded_users = self.db.load_users()
        self.assertEqual(len(loaded_users), 2)
        self.assertEqual(loaded_users[0].email, "student@example.com")
        self.assertEqual(loaded_users[1].email, "instructor@example.com")

    def test_save_and_load_courses(self):
        self.db.save_users([self.student, self.instructor])
        self.db.save_courses([self.course])
        loaded_courses = self.db.load_courses([self.student, self.instructor])

        self.assertEqual(len(loaded_courses), 1)
        self.assertEqual(loaded_courses[0].course_code, "CS101")
        self.assertEqual(loaded_courses[0].course_name, "Introduction to Computer Science")
        self.assertEqual(loaded_courses[0].instructor.email, "instructor@example.com")
        self.assertEqual(loaded_courses[0].student_grades[self.student], "A")


if __name__ == "__main__":
    unittest.main()