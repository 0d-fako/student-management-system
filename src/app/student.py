from src.app.course import Course
from user import User


class Student(User):
    def __init__(self, first_name, last_name, email, hashed_password):
        super().__init__(first_name, last_name, email, hashed_password)
        self.__enrolled_courses: ['Course'] = []
        self.__student_grade = {}

    def view_enrolled_courses(self):
        return self.__enrolled_courses

    def view_course_grade(self, course: Course):
        return self.__enrolled_courses

    def view_instructor_for_course(self, course: Course):
        if course in self.__enrolled_courses:
            return course.get_instructor()

    def display_info(self):
        return f"name: {self.get_full_name()}\n email: {self.get_email()}\ncourses: {self.__enrolled_courses}"

    def remove_courses(self, course):
        self.__enrolled_courses.remove(course)

    def add_courses(self,course):
        self.__enrolled_courses.append(course)

    def get_student_grade(self, course: Course):
        if course not in self.__student_grade:
            return 0.0
        return self.__student_grade[course]




