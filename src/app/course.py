
class Course:
    def __init__(self, course_code: str, course_name:str):
        self._course_code: str = course_code
        self._course_name = course_name
        self._instructor: ['Instructor', None] = None
        self._students: ['Student'] = []