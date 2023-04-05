from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.config import Settings
from fastapi_jwt_auth import AuthJWT


async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session


# @AuthJWT.load_config
# def get_settings() -> Settings:
#     return Settings()
