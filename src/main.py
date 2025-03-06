from src.app.course import Course, CourseGrade
from src.app.student import Student
from src.app.instructor import Instructor
from src.app.database import DatabaseManager

import re

class SystemManagerApp:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
        self.current_user = None
        self.data_manager = DatabaseManager()

    def load_data(self):
        self.students = self.data_manager.load_users('students.txt')
        self.instructors = self.data_manager.load_users('instructors.txt')
        self.courses = self.data_manager.load_courses('courses.txt', self.instructors)

    def save_data(self):
        self.data_manager.save_users('students.txt', self.students)
        self.data_manager.save_users('instructors.txt', self.instructors)
        self.data_manager.save_courses('courses.txt', self.courses)

    def validate_email(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def login(self, email: str, password: str) -> str:
        for student in self.students:
            if student.email == email and student.verify_password(password):
                self.current_user = student
                return "Student"
        
        for instructor in self.instructors:
            if instructor.email == email and instructor.verify_password(password):
                self.current_user = instructor
                return "Instructor"
        return None

    def register_student(self, email: str, password: str, first_name: str, last_name: str) -> str:
        if not self.validate_email(email):
            return "Invalid email format"
        
        for student in self.students:
            if student.email == email:
                return "Email already registered"
        
        new_student = Student(email, password, first_name, last_name)
        self.students.append(new_student)
        self.save_data()
        return "Student registered successfully"

    def register_instructor(self, email: str, password: str, first_name: str, last_name: str) -> str:
        if not self.validate_email(email):
            return "Invalid email format"
        
        for instructor in self.instructors:
            if instructor.email == email:
                return "Email already registered"
        
        new_instructor = Instructor(first_name, last_name, email, password)
        self.instructors.append(new_instructor)
        self.save_data()
        return "Instructor registered successfully"

    def view_courses(self):
        if isinstance(self.current_user, Student):
            return self.current_user.enrolled_courses
        elif isinstance(self.current_user, Instructor):
            return self.current_user.get_course()
        else:
            return "No user logged in"

    def create_course(self, course_code: str, course_name: str, max_capacity: int):
        if isinstance(self.current_user, Instructor):
            new_course = Course(course_code, course_name, self.current_user, max_capacity)
            self.courses.append(new_course)
            self.save_data()
            return "Course created successfully"
        else:
            return "Only instructors can create courses"

    def assign_grade(self, student_email: str, course_code: str, grade: CourseGrade):
        if isinstance(self.current_user, Instructor):
            for course in self.courses:
                if course.course_code == course_code and course.instructor == self.current_user:
                    for student in self.students:
                        if student.email == student_email:
                            course.set_student_grade(student, grade)
                            self.save_data()
                            return "Grade assigned successfully"
            return "Course or student not found"
        else:
            return "Only instructors can assign grades"

    def view_grades(self):
        if isinstance(self.current_user, Student):
            return {course.course_code: course.get_student_grade(self.current_user) for course in self.current_user.enrolled_courses}
        else:
            return "Only students can view grades"

    def run(self):
        self.load_data()
        while True:
            print("\nWelcome to the Student Course Management System")
            print("1. Login")
            print("2. Register as Student")
            print("3. Register as Instructor")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                email = input("Enter email: ")
                password = input("Enter password: ")
                user_type = self.login(email, password)
                if user_type:
                    print(f"Login successful as {user_type}")
                    self.user_menu()
                else:
                    print("Invalid email or password")
            elif choice == '2':
                email = input("Enter email: ")
                password = input("Enter password: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                print(self.register_student(email, password, first_name, last_name))
            elif choice == '3':
                email = input("Enter email: ")
                password = input("Enter password: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                print(self.register_instructor(email, password, first_name, last_name))
            elif choice == '4':
                self.save_data()
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self):
        while True:
            if isinstance(self.current_user, Student):
                print("\nStudent Menu")
                print("1. View Enrolled Courses")
                print("2. View Grades")
                print("3. Logout")
                choice = input("Enter your choice: ")

                if choice == '1':
                    print(self.view_courses())
                elif choice == '2':
                    print(self.view_grades())
                elif choice == '3':
                    self.current_user = None
                    print("Logged out successfully")
                    break
                else:
                    print("Invalid choice. Please try again.")

            elif isinstance(self.current_user, Instructor):
                print("\nInstructor Menu")
                print("1. View Teaching Courses")
                print("2. Create Course")
                print("3. Assign Grade")
                print("4. Logout")
                choice = input("Enter your choice: ")

                if choice == '1':
                    print(self.view_courses())
                elif choice == '2':
                    course_code = input("Enter course code: ")
                    course_name = input("Enter course name: ")
                    max_capacity = int(input("Enter max capacity: "))
                    print(self.create_course(course_code, course_name, max_capacity))
                elif choice == '3':
                    student_email = input("Enter student email: ")
                    course_code = input("Enter course code: ")
                    grade = CourseGrade[input("Enter grade (A, B, C, D, F): ")]
                    print(self.assign_grade(student_email, course_code, grade))
                elif choice == '4':
                    self.current_user = None
                    print("Logged out successfully")
                    break
                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = SystemManagerApp()
    app.run()