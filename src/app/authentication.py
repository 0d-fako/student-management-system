import bcrypt

class AuthenticationService:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        stored_bytes = stored_password.encode('utf-8')
        provided_bytes = provided_password.encode('utf-8')
        return bcrypt.checkpw(provided_bytes, stored_bytes)