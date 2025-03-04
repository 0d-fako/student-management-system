from src.app.course import Course
from src.app.student import Student
from src.app.instructor import Instructor
from src.app.database import DatabaseManager


def main():
    print("Welcome to Code Crunchers School Management System!")

    db_manager = DatabaseManager()
    users = db_manager.load_users()
    courses = db_manager.load_courses(users)

    while True:
        print("\n--- Main Menu ---")
        print("1. Log in as Instructor")
        print("2. Log in as Student")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            instructor = login_as_instructor(users)
            if instructor:
                instructor_menu(instructor, courses, users, db_manager)
        elif choice == "2":
            student = login_as_student(users)
            if student:
                student_menu(student, courses, db_manager)
        elif choice == "3":
            print("Thank you for using the School Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def login_as_instructor(users):
    print("\n--- Instructor Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    for user in users:
        if isinstance(user, Instructor) and user.email == email:
            if user.is_authenticated(email, password):
                print(f"Welcome, {user.name}!")
                return user

    print("Invalid email or password.")
    return None


def login_as_student(users):
    print("\n--- Student Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    for user in users:
        if isinstance(user, Student) and user.email == email:
            if user.is_authenticated(email, password):
                print(f"Welcome, {user.name}!")
                return user

    print("Invalid email or password.")
    return None


def instructor_menu(instructor, courses, users, db_manager):
    while True:
        print("\n--- Instructor Menu ---")
        print("1. Create Course")
        print("2. View My Courses")
        print("3. Assign Grades")
        print("4. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_course(instructor, courses)
        elif choice == "2":
            view_courses(instructor)
        elif choice == "3":
            assign_grades(instructor, courses, users)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


    db_manager.save_users(users)
    db_manager.save_courses(courses)



def student_menu(student, courses, db_manager):
    while True:
        print("\n--- Student Menu ---")
        print("1. View Enrolled Courses")
        print("2. Enroll in a Course")
        print("3. View Grades")
        print("4. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_enrolled_courses(student)
        elif choice == "2":
            enroll_in_course(student, courses)
        elif choice == "3":
            view_grades(student)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

    db_manager.save_users([student])
    db_manager.save_courses(courses)

def create_course(instructor, courses):
    print("\n--- Create a New Course ---")
    course_code = input("Enter course code: ")
    course_name = input("Enter course name: ")

    for existing_course in courses:
        if existing_course.course_code == course_code:
            print("Course code already exists. Please try again.")
            return

    course = Course(course_code, course_name)
    instructor.create_course(course)
    courses.append(course)
    print(f"Course '{course.course_name}' created successfully!")

def view_courses(instructor):
    print("\n--- My Courses ---")
    if not instructor._courses:
        print("No courses found.")
    for course in instructor._courses:
        print(f"- {course.course_code}: {course.course_name}")



def assign_grades(instructor, courses, users):
    print("\n--- Assign Grades ---")
    course_code = input("Enter course code: ")

    course = None
    for c in instructor._courses:
        if c.course_code == course_code:
            course = c
            break

    if course is None:
        print("Course not found.")
        return

    student_email = input("Enter student email: ")

    student = None
    for user in users:
        if isinstance(user, Student) and user.email == student_email:
            student = user
            break

    if student is None or student not in course.get_students():
        print("Student not enrolled in this course.")
        return

    grade = input("Enter grade: ")
    course.student_grades[student] = grade
    print(f"Assigned grade {grade} to {student.name} for {course.course_name}.")


def view_enrolled_courses(student):
    print("\n--- Enrolled Courses ---")
    if not student._courses:
        print("You are not enrolled in any courses.")
    for course in student._courses:
        print(f"- {course.course_code}: {course.course_name}")


def enroll_in_course(student, courses):
    print("\n--- Enroll in a Course ---")
    course_code = input("Enter course code: ")

    course = None
    for c in courses:
        if c.course_code == course_code:
            course = c
            break

    if course is None:
        print("Course not found.")
        return

    try:
        student.enroll_to(course)
        course.add_student(student)
        print(f"Enrolled in {course.course_name} successfully!")
    except ValueError as e:
        print(e)

def view_grades(student):
    print("\n--- View Grades ---")
    if not student._courses:
        print("You have no grades yet.")
    for course in student._courses:
        grade = course.student_grades.get(student, "No grade assigned")
        print(f"- {course.course_code}: {grade}")


if __name__ == "__main__":
    main()
