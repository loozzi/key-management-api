from pydantic import BaseModel


class SignInRequest(BaseModel):
    """
    Request model for sign-in.
    """

    username: str
    password: str


class SignUpRequest(BaseModel):
    """
    Request model for sign-up.
    """

    username: str
    password: str
    email: str


class SignInResponse(BaseModel):
    """
    Response model for sign-in.
    """

    access_token: str
    refresh_token: str
