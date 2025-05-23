from fastapi import APIRouter

from src.configs.settings import AUTH_PREFIX
from src.helpers.response import ResponseModel, response
from src.helpers.validate import remove_special_characters, valid_email, valid_password
from src.schemas.auth import SignInRequest, SignUpRequest, TokenResponse
from src.services.auth import authService

router = APIRouter(prefix=AUTH_PREFIX, tags=["auth"])


# Sign In
@router.post("/sign-in")
async def sign_in(data: SignInRequest) -> ResponseModel[TokenResponse]:
    """
    Sign in endpoint.
    """
    # Validate user credentials
    if not data.username or not data.password:
        return response(400, "Invalid credentials")
    if data.username != remove_special_characters(data.username):
        return response(400, "Invalid username")

    try:
        access_token, refresh_token = authService.sign_in(
            username=data.username,
            password=data.password,
        )
        return response(
            200,
            "User signed in successfully",
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )
    except Exception as e:
        return response(401, str(e))


# Sign Up
@router.post("/sign-up")
async def sign_up(data: SignUpRequest) -> ResponseModel[TokenResponse]:
    """
    Sign up endpoint.
    """
    # Validate user credentials
    if not data.username or not data.password or not data.email:
        return response(400, "Invalid credentials")
    if data.username != remove_special_characters(data.username):
        return response(400, "Invalid username")
    if not valid_email(data.email):
        return response(400, "Invalid email")
    if not valid_password(data.password):
        return response(400, "Invalid password")

    try:
        access_token, refresh_token = authService.sign_up(
            username=data.username,
            password=data.password,
            email=data.email,
        )
        return response(
            200,
            "User signed up successfully",
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )
    except Exception as e:
        return response(401, str(e))


# Sign Out
# Refresh Token
@router.get("/refresh-token")
async def refresh_token(token: str) -> ResponseModel[TokenResponse]:
    """
    Refresh token endpoint.
    """
    try:
        access_token, refresh_token = authService.refresh_token(token=token)
        if not access_token or not refresh_token:
            return response(401, "Invalid token")

        return response(
            200,
            "Token refreshed successfully",
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )
    except Exception as e:
        return response(401, str(e))


# Password Reset
# Password Change


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "url": "/api/v1/auth/health"}
