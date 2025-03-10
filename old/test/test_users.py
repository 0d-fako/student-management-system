import unittest

from app.user import Instructor, Student


class UserTest(unittest.TestCase):
    def test_instructor_can_be_created(self):
        instructor = Instructor("moses@gmail.com", b"{P@sswd}")

    def test_student_can_be_created(self):
        student = Student("student@gmail.com", b"{P@sswd}")

    def test_object_is_instance_of_student(self):
        student = Student("student@gmail.com", b"{P@sswd}")
        self.assertTrue(student.is_student())

    def test_object_is_instance_of_instructor(self):
        instructor = Instructor("student@gmail.com", b"{P@sswd}")
        self.assertTrue(instructor.is_instructor())

if __name__ == '__main__':
    unittest.main()
