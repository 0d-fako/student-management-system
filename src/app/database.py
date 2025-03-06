from src.app.course import Course, CourseGrade
from typing import List, Dict, Tuple, Optional
from src.app.instructor import Instructor
from src.app.student import Student
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
            if not line:
                continue
            try:
                email, first_name, last_name, hashed_password = line.split(',')
                user = User(email, "dummy_password", first_name, last_name)
                user._hashed_password = hashed_password
                users.append(user)
            except ValueError:
                print(f"Warning: Invalid user data format: {line}")
        return users

    @staticmethod
    def save_instructors(filename: str, instructors: List['Instructor']) -> None:
        instructor_data = []
        for instructor in instructors:
            # Store basic user info plus courses taught
            courses_taught = ','.join([course.course_code for course in instructor.view_teaching_courses()])
            instructor_data.append(
                f"{instructor.email},{instructor.first_name},{instructor.last_name},{instructor._hashed_password},{courses_taught}")
        DatabaseManager.save_data(filename, instructor_data)

    @staticmethod
    def load_instructors(filename: str) -> List['Instructor']:
        instructors = []
        instructor_data = DatabaseManager.load_data(filename)
        for line in instructor_data:
            if not line:
                continue
            try:
                parts = line.split(',')
                email, first_name, last_name, hashed_password = parts[:4]
                instructor = Instructor(first_name, last_name, email, "dummy_password")
                instructor._hashed_password = hashed_password
                instructors.append(instructor)
            except ValueError:
                print(f"Warning: Invalid instructor data format: {line}")
        return instructors

    @staticmethod
    def save_students(filename: str, students: List['Student']) -> None:
        student_data = []
        for student in students:
            # Store basic user info plus enrolled courses
            enrolled_courses = ','.join([course.course_code for course in student.view_enrolled_courses()])
            student_data.append(
                f"{student.email},{student.first_name},{student.last_name},{student._hashed_password},{enrolled_courses}")
        DatabaseManager.save_data(filename, student_data)

    @staticmethod
    def load_students(filename: str) -> List['Student']:
        students = []
        student_data = DatabaseManager.load_data(filename)
        for line in student_data:
            if not line:
                continue
            try:
                parts = line.split(',')
                email, first_name, last_name, hashed_password = parts[:4]
                student = Student(email, "dummy_password", first_name, last_name)
                student._hashed_password = hashed_password
                students.append(student)
            except ValueError:
                print(f"Warning: Invalid student data format: {line}")
        return students

    @staticmethod
    def save_courses(filename: str, courses: List['Course']) -> None:
        course_data = []
        for course in courses:
            course_info = f"{course.course_code},{course.course_name},{course.instructor.email if course.instructor else 'None'},{course.max_capacity}"
            enrolled_students = []
            grades = []
            for student, grade in course.enrolled_students.items():
                enrolled_students.append(student.email)
                grades.append(str(grade.value) if grade else "None")
            student_info = ';'.join(enrolled_students)
            grade_info = ';'.join(grades)
            course_data.append(f"{course_info}|{student_info}|{grade_info}")
        DatabaseManager.save_data(filename, course_data)

    @staticmethod
    def load_courses(filename: str, instructors: List['Instructor'], students: List['Student']) -> List['Course']:
        courses = []
        course_data = DatabaseManager.load_data(filename)
        for line in course_data:
            if not line:
                continue
            try:
                parts = line.split('|')
                course_info = parts[0].split(',')
                course_code, course_name, instructor_email, max_capacity = course_info

                instructor = next((inst for inst in instructors if inst.email == instructor_email), None)
                course = Course(course_code, course_name, instructor, int(max_capacity))

                if len(parts) >= 3:
                    student_emails = parts[1].split(';') if parts[1] else []
                    grade_values = parts[2].split(';') if parts[2] else []

                    for i, email in enumerate(student_emails):
                        if email:
                            student = next((s for s in students if s.email == email), None)
                            if student:
                                course.add_student(student)
                                if i < len(grade_values) and grade_values[i] != "None":
                                    try:
                                        grade_value = float(grade_values[i])
                                        grade = next((g for g in CourseGrade if g.value == grade_value), None)
                                        if grade:
                                            course.set_student_grade(student, grade)
                                    except ValueError:
                                        pass
                courses.append(course)
            except ValueError:
                print(f"Warning: Invalid course data format: {line}")
        return courses

    @staticmethod
    def link_entities(courses: List['Course'], instructors: List['Instructor'], students: List['Student']) -> None:
        for course in courses:
            if course.instructor:
                found_instructor = next((i for i in instructors if i.email == course.instructor.email), None)
                if found_instructor:
                    try:
                        found_instructor.create_course(course)
                    except ValueError:
                        pass

        for course in courses:
            for student in course.get_students():
                found_student = next((s for s in students if s.email == student.email), None)
                if found_student and course not in found_student.enrolled_courses:
                    found_student.enrolled_courses.append(course)