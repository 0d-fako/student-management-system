class DatabaseManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_file = f"{data_dir}/users.txt"
        self.courses_file = f"{data_dir}/courses.txt"
        self._create_directory_and_files()
    
    def _create_directory_and_files(self):
        try:
            open(self.users_file, "a").close()
            open(self.courses_file, "a").close()
        except FileNotFoundError:
            try:
                open(self.data_dir + "/dummy.txt", "w").close()
                open(self.users_file, "w").close()
                open(self.courses_file, "w").close()
            except:
                pass 
    
    def save_users(self, users):
        with open(self.users_file, "w") as f:
            for user in users:
                user_type = "instructor" if user.__class__.__name__ == "Instructor" else "student"
                f.write(f"{user.email},{user.hashed_password},{user_type}\n")
    
    def load_users(self):
        from user import Student, Instructor 
        users = []
        try:
            with open(self.users_file, "r") as f:
                for line in f:
                    email, hashed_password, user_type = line.strip().split(",")
                    if user_type == "instructor":
                        user = Instructor(email, hashed_password)
                    else:
                        user = Student(email, hashed_password)
                    users.append(user)
            return users
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
        from course import Course 
    
        courses = []
        try:
            with open(self.courses_file, "r") as f:
                for line in f:
                    course_code, course_name, instructor_email, student_grades_str = line.strip().split(",")
                    
                    instructor = next((user for user in users if user.email == instructor_email), None)
                    if not instructor:
                        print(f"Instructor not found for course: {course_code}")
                        continue
                    
                    course = Course(course_code, course_name, instructor)
                    

                    if student_grades_str != "None":
                        for student_grade in student_grades_str.split(";"):
                            student_email, grade = student_grade.split(":")
                            student = next((user for user in users if user.email == student_email), None)
                            if student:
                                course.add_student(student)
                                course.set_grade(student, grade)
                    
                    courses.append(course)
            return courses
        except Exception as e:
            print(f"Error loading courses: {e}")
            return []