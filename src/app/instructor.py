from src.app.course import Course
from src.app.student import Student


class Instructor:
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        self.__teaching_courses = []

    def create_course(self, course: 'Course'):
        if course in self.__teaching_courses: raise ValueError('Course already exists')
        self.__teaching_courses.append(course)

    def view_students_in_course(self, course: Course):
        return course.get_students()

    def assign_grade(self, student:Student):
        pass


    def set_course(self, course):
        self.__teaching_courses = course

    def get_course(self):
        return self.__teaching_courses
