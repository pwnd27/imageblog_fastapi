from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from datetime import timedelta
from app.config import get_settings
from fastapi_jwt_auth import AuthJWT


settings = get_settings()


class Settings(BaseModel):
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    authjwt_secret_key: str = settings.AUTHJWT_SECRET_KEY
    authjwt_algorithm: str = 'HS256'
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = 'lax'


authjwt = Annotated[AuthJWT, Depends()]


async def current_user(authorize: authjwt) -> str:
    authorize.jwt_required()
    user_email = authorize.get_jwt_subject()
    return user_email # pyright: ignore
    