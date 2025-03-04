

from src.app.course import Course

from abc import ABC
import bcrypt
import re

class UserManager:
    def __init__(self):
        self._users = []

    def register_user(self, user_type, first_name, last_name, email, password):
        if self.email_exists(email):
            raise ValueError("Email already exists in the system")
        
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        if not self._validate_password(password):
            raise ValueError("Password must be at least 8 characters long")
        
        if user_type.lower() == 'student':
            new_user = Student(first_name, last_name, email, password)
        elif user_type.lower() == 'instructor':
            new_user = Instructor(first_name, last_name, email, password)
        else:
            raise ValueError("Invalid user type")
        
        self._users.append(new_user)
        return new_user

    def email_exists(self, email):
        return any(user.email == email for user in self._users)

    def _validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def _validate_password(self, password):
        return len(password) >= 8

    def get_users(self):
        return self._users


class User(ABC):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = self.__encrypt(password)
        self._is_authenticated = False

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return f"{self._first_name} {self._last_name}"

    def is_authenticated(self, email: str, password: str):
        if self._email != email:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self._password)

    def __encrypt(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Student(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        super().__init__(first_name, last_name, email, password)
        self._courses = []
        self._grades = {}

    def enroll_to(self, course):
        if course in self._courses:
            raise ValueError('Already enrolled in this course')
        self._courses.append(course)

    def view_courses(self):
        return self._courses

    def view_course_grade(self, course):
        return self._grades.get(course, "No grade assigned")

    def get_instructors(self):
        return {course: course.instructor for course in self._courses}


class Instructor(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        super().__init__(first_name, last_name, email, password)
        self._courses = []
        self._enrolled_students = {}

    def create_course(self, course):
        if course in self._courses:
            raise ValueError('Course already exists')
        self._courses.append(course)
        course.instructor = self

    def view_courses(self):
        return self._courses

    def view_students(self, course):
        return course.get_students()

    def assign_grade(self, course, student, grade):
        if course not in self._courses:
            raise ValueError("You can only grade students in your own courses")
        if student not in course.get_students():
            raise ValueError("Student is not enrolled in this course")
        student._grades[course] = grade