from src.app.course import Course
from typing import List

from src.app.instructor import Instructor
from src.app.user import User


class DatabaseManager:
    @staticmethod
    def save_data(filename: str, data: List[str]) -> None:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item}\n")

    @staticmethod
    def load_data(filename: str) -> List[str]:
        data = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data.append(line.strip())
        except FileNotFoundError:
            pass
        return data

    @staticmethod
    def save_users(filename: str, users: List['User']) -> None:
        user_data = []
        for user in users:
            user_data.append(f"{user.email},{user.first_name},{user.last_name},{user._hashed_password}")
        DatabaseManager.save_data(filename, user_data)

    @staticmethod
    def load_users(filename: str) -> List['User']:
        users = []
        user_data = DatabaseManager.load_data(filename)
        for line in user_data:
            email, first_name, last_name, hashed_password = line.split(',')
            user = User(email, "dummy_password", first_name, last_name)
            user._hashed_password = hashed_password
            users.append(user)
        return users

    @staticmethod
    def save_courses(filename: str, courses: List['Course']) -> None:
        course_data = []
        for course in courses:
            course_data.append(f"{course.course_code},{course.course_name},{course.instructor.email if course.instructor else 'None'},{course.max_capacity}")
        DatabaseManager.save_data(filename, course_data)

    @staticmethod
    def load_courses(filename: str, instructors: List['Instructor']) -> List['Course']:
        courses = []
        course_data = DatabaseManager.load_data(filename)
        for line in course_data:
            course_code, course_name, instructor_email, max_capacity = line.split(',')
            instructor = next((inst for inst in instructors if inst.email == instructor_email), None)
            course = Course(course_code, course_name, instructor, int(max_capacity))
            courses.append(course)
        return courses