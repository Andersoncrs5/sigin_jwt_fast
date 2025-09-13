import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurado no arquivo .env")

engine = create_engine(DATABASE_URL, echo=True) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from api.models.entities.user_entity import UserEntity
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating tables in db...")
    create_tables()
    print("Tables created!")