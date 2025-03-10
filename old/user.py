from abc import ABC
import bcrypt


class User(ABC):
    def __init__(self, first_name, last_name, email, hashed_password):
        if not first_name:
            raise ValueError("Invalid Name")
        if not last_name:
            raise ValueError("Invalid input")
        if not email:
            raise ValueError("Invalid input")
        self.__full_name = first_name +" "+ last_name
        self.__email = email
        self.__password = self.hash_password(hashed_password)

    def get_full_name(self):
        return self.__full_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def is_authenticated(self, email, password):
        if email != self.__email:
            return False
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def display_info(self):
        pass