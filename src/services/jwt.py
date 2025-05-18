from datetime import datetime, timedelta, timezone

import jwt

from src import environment
from src.repositories.users import UserRepository


class TokenService:
    def __init__(self, secret_key: str, algorithm: str, expiration: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration = int(expiration)
        self.user_repository = UserRepository()

    def create_access_token(self, data: dict) -> tuple[str, str]:
        """
        Create a new access token with the given data.
        The token will be signed with the secret key and algorithm.
        """
        to_encode = data.copy()
        if self.expiration:
            to_encode.update(
                {
                    "exp": int(
                        (
                            datetime.now(timezone.utc)
                            + timedelta(seconds=self.expiration)
                        ).timestamp()
                    )
                }
            )
        to_encode.update({"iat": int(datetime.now(timezone.utc).timestamp())})
        access_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        to_encode.update(
            {"exp": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())}
        )
        to_encode.update({"is_refresh": True})
        refresh_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        # Save the refresh token in the database
        saved = self.user_repository.update_token(
            user_id=data["sub"], token=refresh_token
        )
        if not saved:
            raise ValueError("Failed to save refresh token in the database")

        return access_token, refresh_token

    def decode_access_token(self, token: str, is_refresh: bool = False) -> dict:
        """
        Decode the access token and return the payload.
        If is_refresh is True, it will also check if the user exists in the database.
        """

        if is_refresh:
            __user = self.user_repository.get_by_token(token)
            if not __user:
                raise ValueError("Invalid token")

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")


tokenService = TokenService(
    secret_key=environment.env.JWT_SECRET,
    algorithm=environment.env.JWT_ALGORITHM,
    expiration=environment.env.JWT_EXPIRATION,
)
