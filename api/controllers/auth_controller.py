from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.models.schemas.user_schema import CreateUserDTO, LoginDTO
from api.dependencies.user_dependency import get_user_service
from api.services.user_service import UserService
from fastapi.responses import JSONResponse
from api.utils.res.response_body import ResponseBody
from api.utils.res.tokens import Tokens
from api.models.entities.user_entity import UserEntity
from api.services.jwt_service import create_access_token, create_refresh_token
from api.services.crypto_service import verify_password

app_router = APIRouter(prefix="api/v1/auth")

@app_router.post(
    "/register",
    response_model=ResponseBody[Tokens],
    responses={
        409: {
            "model": ResponseBody[None],
            "description": "Email already exists"
        }
    }
)
def register(dto: CreateUserDTO, user_service: UserService = Depends(get_user_service)):
    if user_service.exists_by_email(dto.email) == True:
        return JSONResponse(
            status_code=409,
            content=dict(ResponseBody[None](
                code=409,
                message="Email already in use",
                status=False,
                body=None
            ))
        )

    user_mapped: UserEntity = dto.to_user_entity()
    user_created = user_service.create(user_mapped)

    token: str = create_access_token(user_created)
    refresh_token = create_refresh_token(user_created)

    user_created = user_service.set_refresh_token(refresh_token, user_created)

    tokens = Tokens(
        token=token,
        refresh_token=refresh_token
    )

    return JSONResponse(
        status_code=201,
        content=dict(ResponseBody[dict](
            message="Welcome",
            code=201,
            status=True,
            body=dict(tokens)
        ))
    )

@app_router.post(
    "/login",
    response_model=ResponseBody[Tokens],
    responses={
        401: {
            "model": ResponseBody[None],
            "description": "Login invalid"
        }
    }
    )
def login(dto: LoginDTO, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_by_email(dto.email)
    if user is None:
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None
            ))
        )

    if verify_password(dto.password,user.password) == False :
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None
            ))
        )

    token: str = create_access_token(user)
    refresh_token = create_refresh_token(user)

    user = user_service.set_refresh_token(refresh_token, user)

    tokens = Tokens(token=token, refresh_token=refresh_token)

    return JSONResponse(
        status_code=201,
        content=dict(ResponseBody[dict](
            message="Welcome again",
            code=201,
            status=True,
            body=dict(tokens)
        ))
    )
    
