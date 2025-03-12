from models import Authentication

class Student:
    def __init__(self, student_id, name, email, password):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = Authentication.encrypt_password(password)

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

