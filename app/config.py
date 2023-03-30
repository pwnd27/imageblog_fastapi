from pydantic import BaseSettings
from pydantic import BaseModel
from datetime import timedelta


class Settings(BaseModel):
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    authjwt_secret_key: str
    authjwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        