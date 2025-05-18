from fastapi import APIRouter

from src.configs.settings import AUTH_PREFIX
from src.helpers.response import ResponseModel, response
from src.helpers.validate import remove_special_characters
from src.schemas.auth import SignInRequest, SignInResponse
from src.services.auth import authService

router = APIRouter(prefix=AUTH_PREFIX, tags=["auth"])


# Sign In
@router.post("/sign-in")
async def sign_in(data: SignInRequest) -> ResponseModel[SignInResponse]:
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
# Sign Out
# Refresh Token
# Password Reset
# Password Change


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "url": "/api/v1/auth/health"}
