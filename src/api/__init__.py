from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.configs.settings import API_V1_PREFIX

api = APIRouter(prefix=API_V1_PREFIX)


api.include_router(auth_router)
