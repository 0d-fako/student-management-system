from app.user import Student


class Course:
    def __init__(self, course_code: str, course_name:str):
        self._course_code: str = course_code
        self._course_name = course_name
        # self._instructor: ['Instructor', None] = None
        self.__instructor = None
        self._students: ['Student'] = []


    def get_students(self):
        return self._students

    def get_instructor(self):
        return self.__instructor

    @property
    def instructor(self):
        return self._instructor

    @instructor.setter
    def instructor(self, instructor: 'Instructor'):
        self._instructor = instructor

    def add_student(self, student: 'Student'):
        self._students.append(student)

    def remove_student(self, student: 'Student'):
        self._students.remove(student)