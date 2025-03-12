from app.course import Course
from typing import List

from app.instructor import Instructor
from app.user import User

class DatabaseManager:
    @staticmethod
    def save_data(filename: str, data: List[str]) -> None:
        try:
            with open(filename, 'w') as file:
                file.writelines([f"{item}\n" for item in data])
        except IOError as e:
            print(f"Error saving data to {filename}: {e}")

    @staticmethod
    def load_data(filename: str) -> List[str]:
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            print(f"File {filename} not found. Returning an empty list.")
            return []
        except IOError as e:
            print(f"Error loading data from {filename}: {e}")
            return []

    @staticmethod
    def save_users(filename: str, users: List['User']) -> None:
        user_data = [f"{user.email},{user.first_name},{user.last_name},{user._hashed_password}" for user in users]
        DatabaseManager.save_data(filename, user_data)

    @staticmethod
    def load_users(filename: str) -> List['User']:
        users = []
        for line in DatabaseManager.load_data(filename):
            try:
                email, first_name, last_name, hashed_password = line.split(',')
                user = User(email, "placeholder", first_name, last_name)
                user._hashed_password = hashed_password
                users.append(user)
            except ValueError as e:
                print(f"Error processing user data: {e}")
        return users

    @staticmethod
    def save_courses(filename: str, courses: List['Course']) -> None:
        course_data = [
            f"{course.course_code},{course.course_name},{course.instructor.email if course.instructor else 'None'},{course.max_capacity}"
            for course in courses
        ]
        DatabaseManager.save_data(filename, course_data)

    @staticmethod
    def load_courses(filename: str, instructors: List['Instructor']) -> List['Course']:
        courses = []
        for line in DatabaseManager.load_data(filename):
            try:
                course_code, course_name, instructor_email, max_capacity = line.split(',')
                instructor = next((inst for inst in instructors if inst.email == instructor_email), None)
                course = Course(course_code, course_name, instructor, int(max_capacity))
                courses.append(course)
            except ValueError as e:
                print(f"Error processing course data: {e}")
        return courses
