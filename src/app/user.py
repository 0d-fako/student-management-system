from abc import ABC

import bcrypt

from app.course import Course


class User(ABC):
    def __init__(self, email: str, password: str):
        self._name = None
        self._email = email
        self._password: bytes = self.__encrypt(password)
        self._is_authenticated = False

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def is_authenticated(self, email: str, password: str):
        if self._email == email: bcrypt.checkpw(password.encode('utf-8'), self._password)

    def __encrypt(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Student(User):
    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._courses: ['Course'] = []

    def is_student(self):
        return isinstance(self, Student)

    def enroll_to(self, course: 'Course'):
        if course in self._courses: raise ValueError('Course already enrolled')
        self._courses.append(course)


class Instructor(User):
    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._courses: ['Course'] = []
        self._enrolled_students: ['Student'] = []

    def is_instructor(self):
        return isinstance(self, Instructor)

    def add_student(self, student: 'Student'):
        self._enrolled_students.append(student)

    def create_course(self, course: 'Course'):
        if course in self._courses: raise ValueError('Course already exists')
        self._courses.append(course)





