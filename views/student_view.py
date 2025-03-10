from models import *

class StudentDashboard:
    @staticmethod
    def display(student):
        while True:
            print("\n=== Student Dashboard ===")
            print("1. View All Courses")
            print("2. View Registered Courses")
            print("3. Enroll in Course")
            print("4. View Course Grades")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                StudentDashboard.view_all_courses()
            elif choice == '2':
                StudentDashboard.view_registered_courses(student)
            elif choice == '3':
                StudentDashboard.enroll_in_course(student)
            elif choice == '4':
                StudentDashboard.view_course_grades(student)
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    @staticmethod
    def view_all_courses():
        courses = DatabaseManager.fetch_all('courses')
        for course in courses:
            instructor = DatabaseManager.filter_records('instructors', 'instructor_id', course['instructor_id'])[0]
            print(f"ID: {course['course_id']}, Title: {course['title']}, Instructor: {instructor['name']}")

    @staticmethod
    def view_registered_courses(student):
        enrollments = DatabaseManager.filter_records('enrollments', 'student_id', student.student_id)
        for enr in enrollments:
            course = DatabaseManager.filter_records('courses', 'course_id', enr['course_id'])[0]
            instructor = DatabaseManager.filter_records('instructors', 'instructor_id', course['instructor_id'])[0]
            grade = enr.get('grade', 'N/A')
            print(f"Course: {course['title']}, Instructor: {instructor['name']}, Grade: {grade}")

    @staticmethod
    def enroll_in_course(student):
        courses = DatabaseManager.fetch_all('courses')
        for course in courses:
            print(f"{course['course_id']}: {course['title']}")
        course_id = input("Enter course ID to enroll: ")

        # Check if already enrolled
        existing = DatabaseManager.filter_records('enrollments', 'student_id', student.student_id)
        if any(enr['course_id'] == course_id for enr in existing):
            print("Already enrolled!")
            return

        enrollment = Enrollment(student.student_id, course_id)
        DatabaseManager.save('enrollments', enrollment)
        print("Enrollment successful!")

    @staticmethod
    def view_course_grades(student):
        enrollments = DatabaseManager.filter_records('enrollments', 'student_id', student.student_id)
        for enr in enrollments:
            course = DatabaseManager.filter_records('courses', 'course_id', enr['course_id'])[0]
            print(f"Course: {course['title']}, Grade: {enr.get('grade', 'N/A')}")
