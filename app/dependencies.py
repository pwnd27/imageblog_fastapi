from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session