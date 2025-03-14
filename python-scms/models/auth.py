import csv
from email_validator import validate_email, EmailNotValidError

import bcrypt

class Authentication:
    @staticmethod
    def encrypt_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def is_valid_password(password, row):
        return bcrypt.checkpw(password.encode(), row['password'].encode())

    @staticmethod
    def verify_user(email, password, user_type):
        filename = f"{user_type}s.csv"
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email and Authentication.is_valid_password(password, row):
                    return True
        return False

    @staticmethod
    def is_valid_email(email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False