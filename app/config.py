from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta


class Settings(BaseSettings):
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    authjwt_secret_key: str
    authjwt_algorithm: str = 'HS256'
    authjwt_token_location: set = {'cookies'}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = 'lax'


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@AuthJWT.load_config # pyright: ignore
def get_config():
    return Settings() # pyright: ignore
