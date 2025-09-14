import os
from dotenv import load_dotenv
from api.models.entities.user_entity import UserEntity
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

if SECRET_KEY == None or ALGORITHM == None or ACCESS_TOKEN_EXPIRE_MINUTES == None or REFRESH_TOKEN_EXPIRE_MINUTES == None :
    raise ValueError("Jwt env are not defined")

def create_access_token(user: UserEntity) -> str:
    if ACCESS_TOKEN_EXPIRE_MINUTES == None or SECRET_KEY == None or ALGORITHM == None:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not defined")
    
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
        "exp": datetime.utcnow() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    }

    token: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(user: UserEntity) -> str:
    if REFRESH_TOKEN_EXPIRE_MINUTES == None or SECRET_KEY == None or ALGORITHM == None:
        raise ValueError("REFRESH_TOKEN_EXPIRE_MINUTES is not defined")
    
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | None:
    if ACCESS_TOKEN_EXPIRE_MINUTES == None or SECRET_KEY == None or ALGORITHM == None:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not defined")

    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        return payload
    except JWTError:
        return None

def extract_user_id(token: str) -> int | None:
    payload = decode_token(token)
    if payload and "sub" in payload:
        return int(payload["sub"])
    return None

def extract_email(token: str) -> str | None:
    payload = decode_token(token)
    if payload and "email" in payload:
        return payload["email"]
    return None

def valid_credentials(creden: HTTPAuthorizationCredentials) -> str:
    scheme = creden.scheme
    if scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header invalid"
        )
    
    token = creden.credentials

    token_valided = decode_token(token)

    if token_valided is None :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header invalid"
        )

    return token
    