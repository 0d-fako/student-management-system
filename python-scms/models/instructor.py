from models import Authentication

class Instructor:
    def __init__(self, instructor_id, name, email, password):
        self.instructor_id = instructor_id
        self.name = name
        self.email = email
        self.password = Authentication.encrypt_password(password)

    def to_dict(self):
        return {
            'instructor_id': self.instructor_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

