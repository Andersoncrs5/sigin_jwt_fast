# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload

import logging
from fastapi import FastAPI
from api.controllers import auth_controller
from api.controllers import user_controller
from api.configs.db.database import create_tables
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    
    create_tables()
    yield
    logger.info("Shutting down the application...")

app.include_router(auth_controller.app_router)
app.include_router(user_controller.app_router)