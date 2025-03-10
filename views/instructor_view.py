from models import *


class InstructorDashboard:
    @staticmethod
    def display(instructor):
        while True:
            print("\n=== Instructor Dashboard ===")
            print("1. View Created Courses")
            print("2. View Registered Students")
            print("3. Grade Student")
            print("4. Create Course")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                InstructorDashboard.view_created_courses(instructor)
            elif choice == '2':
                InstructorDashboard.view_course_students(instructor)
            elif choice == '3':
                InstructorDashboard.grade_student(instructor)
            elif choice == '4':
                InstructorDashboard.create_course(instructor)
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    @staticmethod
    def create_course(instructor):
        print("\n--- Create New Course ---")
        title = input("Enter course title: ")

        course_id = DatabaseManager.get_next_id('courses')
        course = Course(course_id, title, instructor.instructor_id)
        DatabaseManager.save('courses', course)
        print(f"Course created successfully! Course ID: {course.course_id}")

    @staticmethod
    def view_created_courses(instructor):
        courses = DatabaseManager.filter_records('courses', 'instructor_id', instructor.instructor_id)
        print(f"===My Courses ({len(courses)})===")
        print(f"{"ID":<5} | Title")
        print("____________________")
        for course in courses:
            print(f"{course['course_id']:>5} | {course['title']}")

    @staticmethod
    def view_course_students(instructor):
        courses = DatabaseManager.filter_records('courses', 'instructor_id', instructor.instructor_id)
        print("===Registered Students Per Course===")
        print(f"{'Course':<20} | {'Student':<10} | Grade")
        print("_________________________________________")
        for course in courses:
            enrollments = DatabaseManager.filter_records('enrollments', 'course_id', course['course_id'])
            for enr in enrollments:
                student = DatabaseManager.filter_records('students', 'student_id', enr['student_id'])[0]
                print(f"{course['title']:<20} | {student['name']:<10} | {enr.get('grade') if len(enr['grade']) > 0 else 'N/A'}")

    @staticmethod
    def grade_student(instructor):
        courses = DatabaseManager.filter_records('courses', 'instructor_id', instructor.instructor_id)
        for course in courses:
            print(f"{course['course_id']}: {course['title']}")
        course_id = input("Enter course ID: ")

        enrollments = DatabaseManager.filter_records('enrollments', 'course_id', course_id)
        for i, enr in enumerate(enrollments):
            student = DatabaseManager.filter_records('students', 'student_id', enr['student_id'])[0]
            print(f"{i + 1}. Student: {student['name']}, Current Grade: {enr.get('grade', 'N/A')}")

        selection = int(input("Select student number: ")) - 1
        if 0 <= selection < len(enrollments):
            new_grade = input("Enter new grade: ")
            enrollment = Enrollment(
                enrollments[selection]['student_id'],
                enrollments[selection]['course_id'],
                new_grade
            )
            DatabaseManager.update('enrollments', enrollment, 'student_id', enrollment.student_id)
            print("Grade updated!")
        else:
            print("Invalid selection!")