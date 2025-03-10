import unittest

from models import DatabaseManager, Instructor
from views import MainMenu

class TestInstructor(unittest.TestCase):
    def setUp(self):
        DatabaseManager.initialize()

    def test_instructor_can_register(self):
        instructor_id = DatabaseManager.get_next_id('instructors')
        instructor = Instructor(instructor_id, "Daniel", "dan@iel.com", "1234")
        DatabaseManager.save('instructors', instructor)

    def test_cannot_create_duplicate_instructor(self):
        actual = DatabaseManager.is_user_registered("dan@iel.com", "instructors")
        self.assertFalse(actual)
