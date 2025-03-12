import unittest
from src.app.student import Student



class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student("mario", "lee", "adekanbikhalid62@gmail.com", "hashed_password_345")
        self.course1 = Course("computer science", "taiye  more")
        self.course2 = Course("mathematics", "adegboyega. adekanbi")

    def test_view_enrolled_courses(self):
        self.assertEqual(self.student.view_enrolled_courses(), [])
        self.student.add_courses(self.course1)
        self.student.add_courses(self.course2)
        self.assertEqual(self.student.view_enrolled_courses(), [self.course1, self.course2])

    def test_view_instructor_for_course(self):
        self.student.add_courses(self.course1)
        instructor = self.student.view_instructor_for_course(self.course1)
        self.assertEqual(instructor, "khalid")
        self.assertIsNone(self.student.view_instructor_for_course(self.course2))

    def test_display_info(self):
        self.student.add_courses(self.course1)
        info = self.student.display_info()
        self.assertIn("name: adekanbi khalid", info)
        self.assertIn("email: adekanbikhalid62@gmail.com", info)
        self.assertIn("courses", info)
        #

  

if __name__ == "__main__":
    unittest.main()
