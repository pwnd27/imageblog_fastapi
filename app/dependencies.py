from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app import config


async def get_session() -> AsyncSession: # pyright: ignore
    async with async_session() as session:
        async with session.begin():
            yield session
