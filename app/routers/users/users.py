from typing import Any
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_session
from app.routers.users import schemas
from app.routers.users import service
from fastapi_jwt_auth import AuthJWT


router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.CreateUser, session: AsyncSession = Depends(get_session)) -> Any:
    return await service.add_user(user=user, session=session)


@router.post('/login', response_model=None)
async def login(user: schemas.LoginUser, session: AsyncSession = Depends(get_session), Authorize: AuthJWT = Depends()) -> JSONResponse | None:
    user_is_authenthicated = await service.authenticate_user(user=user, session=session)
    if user_is_authenthicated:
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        response = JSONResponse(content={'msg': 'Успешный вход в систему'})
        Authorize.set_access_cookies(access_token, response=response)
        Authorize.set_refresh_cookies(refresh_token, response=response)
        return response
    

@router.post('/refresh')
async def refresh(Authorize: AuthJWT = Depends()) -> JSONResponse:
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user) # pyright: ignore
    response = JSONResponse(content={'msg': 'Токен обновлен'})
    Authorize.set_access_cookies(new_access_token, response=response)
    return response
 

@router.delete('/logout')
async def logout(Authorize: AuthJWT = Depends()) -> JSONResponse:
    Authorize.jwt_required()
    response = JSONResponse(content={'msg': 'Успешный выход из системы'})
    Authorize.unset_jwt_cookies(response=response)
    return response


@router.get('/me')
async def current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {'user': current_user}
