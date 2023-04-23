import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.api import models, service
from app.main import app
from app.api.models import Base, User


@pytest_asyncio.fixture
async def session():

    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True, future=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession # pyright: ignore
    )

    async with async_session() as test_session:
        yield test_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session):
    test_user = User(
        email='test@mail.ru', 
        hashed_password='$2b$12$EAxARHzgjkvqxwZtLhjwYO14skTGQKU68RWuTHnVfH46Uve6TN9Ry' # pass 'qwerty123' # type: ignore
    ) 
    session.add(test_user)
    await session.commit()
    yield test_user


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
        

@pytest_asyncio.fixture(scope='function')
async def user_cookies(client, monkeypatch):
    data = {'email': 'test@mail.ru', 'password': 'qwerty123'}
    async def mock_get_user(email, session) -> models.User:
        return models.User(
            email=data['email'], 
            hashed_password='$2b$12$EAxARHzgjkvqxwZtLhjwYO14skTGQKU68RWuTHnVfH46Uve6TN9Ry'
        )
    monkeypatch.setattr(service, 'get_user', mock_get_user)
        
    response = await client.post('/auth/login', json={
        'email': data['email'],
        'password': data['password'],
    })
    yield response.cookies
