from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOSTNAME: str
    DATABASE_PORT: int
    POSTGRES_DB: str

    AUTHJWT_SECRET_KEY: str

    class Config:
        env_file = './.env'

@lru_cache()
def get_settings() -> Settings:
    return Settings() # pyright: ignore
