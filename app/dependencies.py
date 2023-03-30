from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Settings
from fastapi_jwt_auth import AuthJWT


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@AuthJWT.load_config
def get_settings() -> Settings:
    return Settings()
