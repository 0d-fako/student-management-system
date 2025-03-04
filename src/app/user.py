from abc import ABC

from app.course import Course


class User(ABC):
    def __init__(self, email: str, password: bytes):
        self._name = None
        self._email = email
        self._password = password
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




class Student(User):
    def __init__(self, email: str, password: bytes):
        super().__init__(email, password)
        self._courses: ['Course'] = []

    def is_student(self):
        return isinstance(self, Student)


class Instructor(User):
    def __init__(self, email: str, password: bytes):
        super().__init__(email, password)
        self._courses: ['Course'] = []
        self._enrolled_students: ['Student'] = []

    def is_instructor(self):
        return isinstance(self, Instructor)




