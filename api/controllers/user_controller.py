from fastapi import APIRouter, Depends
from api.services.jwt_service import *
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.models.schemas.user_schema import UpdateUserDTO
from api.dependencies.user_dependency import get_user_service
from api.services.user_service import UserService
from fastapi.responses import JSONResponse
from api.utils.res.response_body import ResponseBody
from api.utils.res.responses_http import *
from api.models.schemas.user_schema import UserOUT

app_router = APIRouter(prefix="/api/v1/user", tags=["User"])

bearer_scheme = HTTPBearer()

@app_router.get(
    "",
    status_code=200,
    response_model=ResponseBody[UserOUT],
    responses={
        404: responses_404_user,
        401: responses_401
    }
)
def me(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):

    token = valid_credentials(credentials)

    user_id = extract_user_id(token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None
            ))
        )

    user = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                status=False,
                body=None
            ))
        )
    
    userDto = user.to_user_out()

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                code=status.HTTP_200_OK,
                message="User found with successfully",
                status=True,
                body=dict(userDto)
            ))
        )

@app_router.delete(
    "",
    status_code=200,
    response_model=ResponseBody[None],
    responses={
        404: responses_404_user,
        401: responses_401
    }
)
def delete(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):

    token = valid_credentials(credentials)

    user_id = extract_user_id(token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None
            ))
        )

    user = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                status=False,
                body=None
            ))
        )
    
    user_service.delete(user)

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                code=status.HTTP_200_OK,
                message="Bye Bye",
                status=True,
                body=None
            ))
        )

@app_router.put(
    "",
    status_code=200,
    response_model=ResponseBody[UserOUT],
    responses={
        404: responses_404_user,
        401: responses_401
    }
)
def update(
    dto: UpdateUserDTO,
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):

    token = valid_credentials(credentials)

    user_id = extract_user_id(token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None
            ))
        )

    user = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                status=False,
                body=None
            ))
        )
    
    user_updated = user_service.update(user, dto)

    user_dto = user_updated.to_user_out()

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                code=status.HTTP_200_OK,
                message="User updated with successfully",
                status=True,
                body=dict(user_dto)
            ))
        )
