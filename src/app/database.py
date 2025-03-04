from src.app.user import Student, Instructor, UserManager
from src.app.course import Course

class DatabaseManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_file = f"{data_dir}/users.txt"
        self.courses_file = f"{data_dir}/courses.txt"
        self._create_directory_and_files()
    
    def _create_directory_and_files(self):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            open(self.users_file, "a").close()
            open(self.courses_file, "a").close()
        except Exception as e:
            print(f"Error creating directories: {e}")
    
    def save_users(self, users):
        with open(self.users_file, "w") as f:
            for user in users:
                user_type = "instructor" if isinstance(user, Instructor) else "student"
                f.write(f"{user._first_name},{user._last_name},{user.email},{user._password.decode('utf-8')},{user_type}\n")
    
    def load_users(self):
        user_manager = UserManager()
        try:
            with open(self.users_file, "r") as f:
                for line in f:
                    first_name, last_name, email, password, user_type = line.strip().split(",")
                    try:
                        user_manager.register_user(user_type, first_name, last_name, email, password)
                    except ValueError as e:
                        print(f"Error loading user: {e}")
            return user_manager.get_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def save_courses(self, courses):
        with open(self.courses_file, "w") as f:
            for course in courses:
                instructor_email = course.instructor.email if course.instructor else "None"
                student_grades = ";".join([f"{student.email}:{grade}" for student, grade in course.student_grades.items()])
                f.write(f"{course.course_code},{course.course_name},{instructor_email},{student_grades}\n")
    
    def load_courses(self, users):
        courses = []
        try:
            with open(self.courses_file, "r") as f:
                for line in f:
                    course_code, course_name, instructor_email, student_grades_str = line.strip().split(",")
                    
                    # Find instructor
                    instructor = next((user for user in users if user.email == instructor_email), None)
                    
                    # Create course
                    course = Course(course_code, course_name)
                    if instructor:
                        instructor.create_course(course)
                    
                    # Add students and grades
                    if student_grades_str != "None":
                        for student_grade in student_grades_str.split(";"):
                            student_email, grade = student_grade.split(":")
                            student = next((user for user in users if user.email == student_email), None)
                            if student:
                                student.enroll_to(course)
                                student._grades[course] = grade
                    
                    courses.append(course)
            return courses
        except Exception as e:
            print(f"Error loading courses: {e}")
            return []