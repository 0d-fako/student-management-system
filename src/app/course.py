from enum import Enum
from typing import Dict, Optional, List


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
        self.enrolled_students: Dict['Student', Optional[CourseGrade]] = {}

    def add_student(self, student: 'Student') -> bool:
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

    def get_students(self) -> List['Student']:
        return list(self.enrolled_students.keys())

    def get_course_id(self) -> str:
        return self.course_code

    def get_course_name(self) -> str:
        return self.course_name

    def get_instructor(self):
        return self.instructor

    def is_full(self) -> bool:
        return len(self.enrolled_students) >= self.max_capacity

    def get_enrollment_count(self) -> int:
        return len(self.enrolled_students)


