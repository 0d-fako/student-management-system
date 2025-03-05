from src.app.authentication import AuthenticationService


class User:
    def __init__(self, email: str, password: str, first_name: str = '', last_name: str = ''):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self._hashed_password = AuthenticationService.hash_password(password)
        self._is_authenticated = False

    def is_authenticated(self) -> bool:
        return self._is_authenticated

    def verify_password(self, password: str) -> bool:
        is_correct = AuthenticationService.verify_password(
            self._hashed_password, 
            password
        )
        self._is_authenticated = is_correct
        return is_correct

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self) -> str:
        return f"User(email={self.email}, name={self.get_full_name()})"