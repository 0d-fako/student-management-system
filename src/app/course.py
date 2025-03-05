from enum import Enum
from typing import Dict, Optional

from src.app.student import Student


class CourseGrade(Enum):
    A = 4.0
    B = 3.0
    C = 2.0
    D = 1.0
    F = 0.0


class Course:
    def __init__(self, course_code: str, course_name: str, instructor=None, max_capacity: int = 30):
        self.course_code = course_code
        self.course_name = course_name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.enrolled_students: Dict[Student, Optional[CourseGrade]] = {}

    def add_student(self, student) -> bool:
        if len(self.enrolled_students) < self.max_capacity:
            self.enrolled_students[student] = None
            return True
        return False

    def remove_student(self, student) -> bool:
        if student in self.enrolled_students:
            del self.enrolled_students[student]
            return True
        return False

    def set_student_grade(self, student, grade: CourseGrade):
        if student in self.enrolled_students:
            self.enrolled_students[student] = grade

    def get_student_grade(self, student) -> Optional[CourseGrade]:
        return self.enrolled_students.get(student)
