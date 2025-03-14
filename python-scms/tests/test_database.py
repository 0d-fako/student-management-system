import tempfile
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import DatabaseManager, DATABASE_CONFIG


class TestDatabaseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        for key in DATABASE_CONFIG.keys():
            DATABASE_CONFIG[key] = os.path.join(cls.temp_dir.name, f"{key}.csv")
        DatabaseManager.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def setUp(self):
        tables = {
            'students': ['student_id', 'name', 'email', 'password'],
            'instructors': ['instructor_id', 'name', 'email', 'password'],
            'courses': ['course_id', 'title', 'instructor_id'],
            'enrollments': ['student_id', 'course_id', 'grade'],
        }
        for table, headers in tables.items():
            path = DATABASE_CONFIG[table]
            with open(path, 'w') as file:
                file.write(','.join(headers) + '\n')

    def test_initialize_creates_files(self):
        for table, path in DATABASE_CONFIG.items():
            self.assertTrue(os.path.exists(path), f"{path} does not exist")

    def test_save_and_fetch_all(self):
        class Student:
            def __init__(self, student_id, name, email, password):
                self.student_id = student_id
                self.name = name
                self.email = email
                self.password = password

            def to_dict(self):
                return {
                    'student_id': self.student_id,
                    'name': self.name,
                    'email': self.email,
                    'password': self.password
                }

        student = Student(1, 'Test Student', 'test@student.com', 'password123')
        DatabaseManager.save('students', student)

        records = DatabaseManager.fetch_all('students')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['name'], 'Test Student')

    def test_update_record(self):
        class Student:
            def __init__(self, student_id, name, email, password):
                self.student_id = student_id
                self.name = name
                self.email = email
                self.password = password

            def to_dict(self):
                return {
                    'student_id': self.student_id,
                    'name': self.name,
                    'email': self.email,
                    'password': self.password
                }

        student = Student(1, 'Test Student', 'test@student.com', 'password123')
        DatabaseManager.save('students', student)

        updated_student = Student(1, 'Updated Student', 'updated@student.com', 'newpassword456')
        DatabaseManager.update('students', updated_student, 'student_id', '1')

        records = DatabaseManager.fetch_all('students')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['name'], 'Updated Student')

    def test_delete_record(self):
        class Student:
            def __init__(self, student_id, name, email, password):
                self.student_id = student_id
                self.name = name
                self.email = email
                self.password = password

            def to_dict(self):
                return {
                    'student_id': self.student_id,
                    'name': self.name,
                    'email': self.email,
                    'password': self.password
                }

        student = Student(1, 'Test Student', 'test@student.com', 'password123')
        DatabaseManager.save('students', student)

        DatabaseManager.delete('students', 'student_id', '1')

        records = DatabaseManager.fetch_all('students')
        self.assertEqual(len(records), 0)

    def test_filter_records(self):
        class Student:
            def __init__(self, student_id, name, email, password):
                self.student_id = student_id
                self.name = name
                self.email = email
                self.password = password

            def to_dict(self):
                return {
                    'student_id': self.student_id,
                    'name': self.name,
                    'email': self.email,
                    'password': self.password
                }

        student1 = Student(1, 'Student One', 'one@student.com', 'password123')
        student2 = Student(2, 'Student Two', 'two@student.com', 'password456')
        DatabaseManager.save('students', student1)
        DatabaseManager.save('students', student2)

        filtered = DatabaseManager.filter_records('students', 'email', 'one@student.com')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'Student One')

    def test_is_user_registered(self):
        class Student:
            def __init__(self, student_id, name, email, password):
                self.student_id = student_id
                self.name = name
                self.email = email
                self.password = password

            def to_dict(self):
                return {
                    'student_id': self.student_id,
                    'name': self.name,
                    'email': self.email,
                    'password': self.password
                }

        student = Student(1, 'Test Student', 'test@student.com', 'password123')
        DatabaseManager.save('students', student)

        self.assertTrue(DatabaseManager.is_user_registered('test@student.com', 'student'))
        self.assertFalse(DatabaseManager.is_user_registered('nonexistent@student.com', 'student'))