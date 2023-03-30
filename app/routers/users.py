from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT
import schemas


router = APIRouter()


@router.post('/signup')
async def signup():
    pass



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