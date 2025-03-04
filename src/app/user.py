from course import Course


class User:
    def __init__(self, email: str, password: bytes):
        self._email = email
        self._password = password
        self._is_authenticated = False


class Student(User):
    pass


class Instructor(User):
    def __init__(self, email: str, password: bytes):
        super().__init__(email, password)
        self._courses: [Course] = []
        self._enrolled_students: [Student] = []



