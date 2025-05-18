import bcrypt

from src.repositories.users import UserRepository
from src.services.jwt import tokenService


class AuthService:
    def __init__(self):
        self.token_service = tokenService
        self.user_repository = UserRepository()

    def sign_in(self, username: str, password: str) -> tuple[str, str]:
        """
        Sign in user and return access and refresh tokens.
        """
        # Here you would typically validate the user's credentials
        # For example, check against a database
        # This is a placeholder implementation
        password_hash = self.user_repository.get_password(username)
        if not password_hash:
            raise ValueError("Invalid credentials")

        password_checked = bcrypt.checkpw(password.encode(), password_hash.encode())
        if not password_checked:
            raise ValueError("Invalid credentials")

        user = self.user_repository.get_by_username(username)

        if user:
            access_token, refresh_token = self.token_service.create_access_token(
                data={"sub": user["username"]}
            )
            return access_token, refresh_token
        else:
            raise ValueError("Invalid credentials")


authService = AuthService()
