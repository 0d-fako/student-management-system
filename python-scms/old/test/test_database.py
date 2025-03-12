import unittest
import os
from app.course import Course
from app.instructor import Instructor
from app.user import User
from app.database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = "test_data.txt"
        self.temp_users_file = "test_users.txt"
        self.temp_courses_file = "test_courses.txt"

        self.mock_user = User("test@example.com", "password123", "Test", "User")
        self.mock_user._hashed_password = "hashed_password"

        self.mock_instructor = Instructor("instructor@example.com", "password123", "Instructor", "Test")
        self.mock_course = Course("CS101", "Intro to Computer Science", self.mock_instructor, 30)

    def tearDown(self):
        # Clean up temporary files
        for file in [self.temp_file, self.temp_users_file, self.temp_courses_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_save_and_load_data(self):
        data = ["line1", "line2", "line3"]
        DatabaseManager.save_data(self.temp_file, data)
        loaded_data = DatabaseManager.load_data(self.temp_file)
        self.assertEqual(data, loaded_data)

    def test_save_and_load_users(self):
        users = [self.mock_user]
        DatabaseManager.save_users(self.temp_users_file, users)
        loaded_users = DatabaseManager.load_users(self.temp_users_file)
        self.assertEqual(len(users), len(loaded_users))
        self.assertEqual(users[0].email, loaded_users[0].email)
        self.assertEqual(users[0].first_name, loaded_users[0].first_name)

    def test_save_and_load_courses(self):
        instructors = [self.mock_instructor]
        courses = [self.mock_course]
        DatabaseManager.save_courses(self.temp_courses_file, courses)
        loaded_courses = DatabaseManager.load_courses(self.temp_courses_file, instructors)
        self.assertEqual(len(courses), len(loaded_courses))
        self.assertEqual(courses[0].course_code, loaded_courses[0].course_code)
        self.assertEqual(courses[0].instructor.email, loaded_courses[0].instructor.email)

    def test_load_nonexistent_file(self):
        non_existent_file = "non_existent.txt"
        loaded_data = DatabaseManager.load_data(non_existent_file)
        self.assertEqual(loaded_data, [])

