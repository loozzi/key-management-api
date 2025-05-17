import os

from dotenv import load_dotenv

load_dotenv(".env")


class ProdConfig:
    """
    Configuration for the development environment.
    """

    # General
    APP_NAME = "Key Management System"
    APP_VERSION = "1.0.0"
    DEBUG = True
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 80)

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME", "mydb")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION = os.getenv("JWT_EXPIRATION", 3600)  # 1 hour
