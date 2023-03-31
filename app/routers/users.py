from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session
import schemas
import service


router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, summary='Create new user', response_model=schemas.UserBase)
async def signup(user: schemas.CreateUser, session: AsyncSession = Depends(get_session)):
    db_user = await service.get_user(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой уже существует',
        )
    return await service.create_user(session=session, user=user)


# @router.post('/login')
# def login(user: schemas.LoginUser, Authorize: AuthJWT = Depends()) -> dict:
#     if user.email != "123@mail.ru" or user.password != "testtest":
#         raise HTTPException(status_code=401,detail="Неверная почта или пароль")

#     access_token = Authorize.create_access_token(subject=user.email)
#     refresh_token = Authorize.create_refresh_token(subject=user.email)
#     return {"access_token": access_token, "refresh_token": refresh_token}

# @router.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()) -> dict:
#     Authorize.jwt_refresh_token_required()

#     current_user = Authorize.get_jwt_subject()
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     return {"access_token": new_access_token}
