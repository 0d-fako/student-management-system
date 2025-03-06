from typing import List

from src.app.course import Course, CourseGrade
from src.app.user import User


class Instructor(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        super().__init__(email, password, first_name, last_name)
        self.teaching_courses: List['Course'] = []

    def create_course(self, course_code: str, course_name: str, max_capacity: int):
        if any(course.course_code == course_code for course in self.teaching_courses):
            raise ValueError("Course code already exists.")
        new_course = Course(course_code, course_name, self, max_capacity)
        self.teaching_courses.append(new_course)
        return new_course

    def view_teaching_courses(self) -> List['Course']:
        return self.teaching_courses

    def view_students_in_course(self, course: 'Course') -> List['Student']:
        if course not in self.teaching_courses:
            raise ValueError("You are not teaching this course")
        return course.get_students()

    def assign_grade(self, student: 'Student', course: 'Course', course_grade: 'CourseGrade'):
        if course not in self.teaching_courses:
            raise ValueError("You are not teaching this course")
        if student not in course.get_students():
            raise ValueError("Student is not enrolled in this course")
        course.set_student_grade(student, course_grade)

    def get_course(self) -> List['Course']:
        return self.teaching_courses