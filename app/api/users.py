from typing import Annotated, Any
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.api import schemas
from app.api import crud
from app.utils import verify_password


async_session = Annotated[AsyncSession, Depends(get_session)]
authjwt = Annotated[AuthJWT, Depends()]

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.CreateUser, session: async_session) -> Any:
    if user.password != user.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пароли не совпадают'
        )
    user_in_db = await crud.get_user(email=user.email, session=session)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой уже существует',
        )
    return await crud.create_user(user=user.dict(), session=session)


@router.post('/login', response_model=None)
async def login(user: schemas.LoginUser, session: async_session, authorize: authjwt) -> JSONResponse | None:
    credentialials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль",
        )
    user_in_db = await crud.get_user(email=user.email, session=session)
    if not user_in_db:
        raise credentialials_exception
    if not await verify_password(user.password, user_in_db.hashed_password):
        raise credentialials_exception
    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    response = JSONResponse(content={'msg': 'Успешный вход в систему'})
    authorize.set_access_cookies(access_token, response=response)
    authorize.set_refresh_cookies(refresh_token, response=response)
    return response


@router.post('/refresh')
async def refresh(authorize: authjwt) -> JSONResponse:
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user) # pyright: ignore
    response = JSONResponse(content={'msg': 'Токен обновлен'})
    authorize.set_access_cookies(new_access_token, response=response)
    return response
 

@router.delete('/logout')
async def logout(authorize: authjwt) -> JSONResponse:
    authorize.jwt_required()
    response = JSONResponse(content={'msg': 'Успешный выход из системы'})
    authorize.unset_jwt_cookies(response=response)
    return response


@router.get('/me', response_model=schemas.User)
async def current_user(authorize: authjwt) -> Any:
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    return {'user': current_user}
