class Course:
    def __init__(self, course_id, title, instructor_id):
        self.course_id = course_id
        self.title = title
        self.instructor_id = instructor_id

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'title': self.title,
            'instructor_id': self.instructor_id
        }
