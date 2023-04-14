from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.users import schemas
from app.routers.users import crud
from app import models
from app.utils import verify_password


async def add_user(user: schemas.CreateUser, session: AsyncSession) -> models.User:
    db_user = await crud.get_user(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой уже существует',
        )
    return await crud.create_user(session=session, user=user)


async def authenticate_user(user: schemas.LoginUser, session: AsyncSession) -> bool:
    db_user = await crud.get_user(session=session, email=user.email)
    if not db_user or not await verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль",
        )
    return True
