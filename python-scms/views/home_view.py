import sys
from models import *
from views import *


class MainMenu:
    @staticmethod
    def display():
        while True:
            print("\n=== Main Menu ===")
            print("1. Login")
            print("2. Register Student")
            print("3. Register Instructor")
            print("4. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                email = input("Email: ")
                if not Authentication.is_valid_email(email):
                    print("Invalid Email")
                    print("Going back to main menu.")
                    continue
                password = input("Password: ")
                is_student = input("Are you a student (y/n): ").lower().startswith('y')
                if Authentication.verify_user(email, password, "student" if is_student else "instructor"):
                    MainMenu.display_dashboard(email, is_student)
                else:
                    print("Invalid credentials!")
            elif choice == '2':
                MainMenu.register_student()
            elif choice == '3':
                MainMenu.register_instructor()
            elif choice == '4':
                sys.exit()
            else:
                print("Invalid choice!")

    @staticmethod
    def display_dashboard(email, is_student):
        StudentDashboard.display(MainMenu.get_student(email)) if is_student else InstructorDashboard.display(
            MainMenu.get_instructor(email))

    @staticmethod
    def get_student(email):
        students = DatabaseManager.fetch_all('students')
        for student in students:
            if student['email'] == email:
                return Student(student['student_id'], student['name'], student['email'], '')
        return None

    @staticmethod
    def get_instructor(email):
        instructors = DatabaseManager.fetch_all('instructors')
        for instructor in instructors:
            if instructor['email'] == email:
                return Instructor(instructor['instructor_id'], instructor['name'], instructor['email'], '')
        return None

    @staticmethod
    def register_student():
        name = input("Fullname: ")
        email = input("Email: ")
        if not Authentication.is_valid_email(email):
            print("\nInvalid Email. start over again. be careful next time!\n")
            MainMenu.register_student()

        password = input("Password: ")
        if DatabaseManager.is_user_registered(email, 'student'):
            print("Email already registered!")
            option = input("Do you wish to try again? (y/n): ").lower()
            if option.startswith('y'): MainMenu.register_student()
            else: return

        student_id = DatabaseManager.get_next_id('students')
        student = Student(student_id, name, email, password)
        DatabaseManager.save('students', student)
        print("Registration successful!")

    @staticmethod
    def register_instructor():
        name = input("Fullname: ")
        email = input("Email: ")
        if not Authentication.is_valid_email(email):
            print("\nInvalid Email. Start over again. be careful next time!\n")
            MainMenu.register_instructor()
        if DatabaseManager.is_user_registered(email, 'instructor'):
            print("Email already registered!")
            option = input("Do you wish to try again? (y/n): ").lower()
            if option.startswith('y'): MainMenu.register_instructor()
            elif option.startswith('n'): MainMenu.display()
            else:
                print("Invalid choice! Taking you back to main menu")
        password = input("Password: ")


        instructor_id = DatabaseManager.get_next_id('instructors')
        instructor = Instructor(instructor_id, name, email, password)
        DatabaseManager.save('instructors', instructor)
        print("Registration successful!")
