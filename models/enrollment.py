class Enrollment:
    def __init__(self, student_id, course_id, grade=None):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'course_id': self.course_id,
            'grade': self.grade or ''
        }