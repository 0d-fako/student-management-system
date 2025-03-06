from src.app.user import Student


class Course:
    def __init__(self, course_code: str, course_name: str):
        self._course_code: str = course_code
        self._course_name: str = course_name
        self._instructor = None
        self._students: list = []

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def course_name(self) -> str:
        return self._course_name

    @property
    def instructor(self):
        return self._instructor

    @instructor.setter
    def instructor(self, instructor):
        self._instructor = instructor

    def enroll_student(self, student):
        if student in self._students:
            raise ValueError(f"Student {student.name} is already enrolled in this course.")
        student.enroll_to(self)
        self._students.append(student)

    def unenroll_student(self, student):
        if student not in self._students:
            raise ValueError(f"Student {student.name} is not enrolled in this course.")
        student.remove_course(self)
        self._students.remove(student)

    def get_students(self) -> list:
        return self._students

    def assign_grade(self, student, grade: float):
        if student not in self._students:
            raise ValueError(f"Student {student.name} is not enrolled in this course.")
        student.assign_grade(self, grade)

    def get_grades(self) -> dict:
        grades = {}
        for student in self._students:
            grades[student.email] = student.get_student_grade(self)
        return grades

    def __str__(self):
        instructor_name = self._instructor.name if self._instructor else "No instructor"
        return f"Course: {self._course_code} - {self._course_name} (Instructor: {instructor_name})"
