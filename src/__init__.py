import logging
import sys

import uvicorn
from fastapi import FastAPI

from src.configs import Environment

if len(sys.argv) > 1 and sys.argv[1] == "--dev":
    env = "dev"
else:
    env = "prod"
environment = Environment(env)

app = FastAPI(title=environment.env.APP_NAME)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Environment: {environment.name}")
logger.info(f"Description: {environment.description}")
logger.info(uvicorn.Config.asgi_version)

logger.info(f"Host: {environment.env.HOST}")
logger.info(f"Port: {environment.env.PORT}")
logger.info(f"Debug: {environment.env.DEBUG}")

logger.info("Starting FastAPI application...")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
