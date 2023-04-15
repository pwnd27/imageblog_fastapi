from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./imageblog.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) # pyright: ignore


async def get_session() -> AsyncSession: # pyright: ignore
    async with async_session() as session:
        async with session.begin():
            yield session
