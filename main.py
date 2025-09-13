# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload

import logging
from fastapi import FastAPI
from api.controllers import auth_controller
from api.configs.db.database import create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def start_up():
    create_tables()

app.include_router(auth_controller.app_router)