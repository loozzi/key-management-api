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
        :param username: Username of the user
        :param password: Password of the user
        :return: Access and refresh tokens
        :raises ValueError: If the credentials are invalid
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
                data={"sub": str(user["id"]), "username": user["username"]}
            )
            return access_token, refresh_token
        else:
            raise ValueError("Invalid credentials")

    def sign_up(self, username: str, password: str, email: str) -> tuple[str, str]:
        """
        Sign up user and return access and refresh tokens.
        :param username: Username of the user
        :param password: Password of the user
        :param email: Email of the user
        :return: Access and refresh tokens
        :raises ValueError: If the credentials are invalid
        :raises Exception: If the user already exists
        """
        # Here you would typically create a new user in the database
        # This is a placeholder implementation
        if self.user_repository.get_by_username(username):
            raise ValueError("Username already exists")
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already exists")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if self.user_repository.create_user(username, password_hash, email):
            user = self.user_repository.get_by_username(username)
            if not user:
                raise ValueError("User not found")

            access_token, refresh_token = self.token_service.create_access_token(
                data={"sub": str(user["id"]), "username": user["username"]}
            )
            return access_token, refresh_token
        else:
            raise ValueError("Failed to create user")

    def refresh_token(self, token: str) -> tuple[str, str]:
        """
        Refresh the access token using the refresh token.
        :param token: Refresh token
        :return: New access and refresh tokens
        :raises ValueError: If the token is invalid
        :raises Exception: If the user is not found
        """
        # Here you would typically validate the refresh token and issue a new access token
        # This is a placeholder implementation
        payload = self.token_service.decode_access_token(token, is_refresh=True)
        if not payload:
            raise ValueError("Invalid token")

        user = self.user_repository.get_by_id(payload["sub"])
        if not user:
            raise ValueError("User not found")

        access_token, refresh_token = self.token_service.create_access_token(
            data={"sub": user["id"], "username": user["username"]}
        )
        return access_token, refresh_token


authService = AuthService()
