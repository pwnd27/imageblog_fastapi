import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.models import Base, User


@pytest_asyncio.fixture(scope='function')
async def db_session():

    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True, future=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession # pyright: ignore
    )

    async with async_session() as session:
        session.add(User(email='test@mail.ru', hashed_password='qwerty123'))
        await session.flush()
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def client():
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client

# @pytest_asyncio.fixture(scope='function')
# async def user(db_session):
#     user = User(email='test@mail.ru', hashed_password='qwerty123')
#     db_session.add(user)
#     await db_session.flush()
#     return user
