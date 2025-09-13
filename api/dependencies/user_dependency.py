from fastapi import Depends
from sqlalchemy.orm import Session
from api.services.user_service import UserService
from api.configs.db.database import get_db

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)