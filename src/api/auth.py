from fastapi import APIRouter

from src.configs.settings import AUTH_PREFIX

router = APIRouter(prefix=AUTH_PREFIX, tags=["auth"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "url": "/api/v1/auth/health"}
