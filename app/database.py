from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


settings = get_settings()

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://' \
                          f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
                          f'@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) # pyright: ignore


async def get_session() -> AsyncSession: # pyright: ignore
    async with async_session() as session:
        async with session.begin():
            yield session
