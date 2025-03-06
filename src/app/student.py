from typing import List

from src.app.user import User


class Student(User):
    def __init__(self, email: str, password: str, first_name: str = '', last_name: str = ''):
        super().__init__(email, password, first_name, last_name)
        self.enrolled_courses: List['Course'] = []

    def enroll_in_course(self, course: 'Course') -> bool:
        if course.add_student(self) and course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            return True
        return False

    def drop_course(self, course: 'Course') -> bool:
        if course in self.enrolled_courses:
            course.remove_student(self)
            self.enrolled_courses.remove(course)
            return True
        return False

    def view_enrolled_courses(self) -> List['Course']:
        return self.enrolled_courses

    def calculate_gpa(self) -> float:
        if not self.enrolled_courses:
            return 0.0

        total_grade_points = sum(
            course.get_student_grade(self).value
            for course in self.enrolled_courses
            if course.get_student_grade(self) is not None
        )
        return total_grade_points / len(self.enrolled_courses)


