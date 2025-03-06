from typing import List

from src.app.course import Course
from src.app.student import Student
from src.app.user import User

class Instructor(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        super().__init__(email, password, first_name, last_name)
        self.__teaching_courses = []

    def create_course(self, course: Course):
        if course in self.__teaching_courses:
            raise ValueError('Course already exists')
        self.__teaching_courses.append(course)

    def view_teaching_courses(self) -> List[Course]:
        return self.__teaching_courses

    def view_students_in_course(self, course: Course) -> List[Student]:
        if course not in self.__teaching_courses:
            raise ValueError("You are not teaching this course")
        return course.get_students()

    def assign_grade(self, student: Student, course: Course, grade: float):
        if course not in self.__teaching_courses:
            raise ValueError("You are not teaching this course")
        if student not in course.get_students():
            raise ValueError("Student is not enrolled in this course")
        course.set_student_grade(student, grade)

    def get_course(self) -> List[Course]:
        return self.__teaching_courses