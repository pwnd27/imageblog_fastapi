import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import AsyncClient
from app.main import app
from app.routers.users import crud
from app import models
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from app.routers.users import schemas


@pytest.mark.asyncio
async def test_create_user_should_return_error400_when_user_exist(monkeypatch: MonkeyPatch) -> None:
    data = {'email': 'test12@mail.ru', 'password': 'testtest', 'password_confirm': 'testtest'}
 
    async def mock_get_user(session: AsyncSession, email: EmailStr) -> models.User:
        return models.User(email='test12@mail.ru', hashed_password='testtest')
 
    monkeypatch.setattr(crud, 'get_user', mock_get_user)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/signup", json=data)
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_user_when_not_exist_in_db(monkeypatch: MonkeyPatch) -> None:
    data = {'email': 'test12@mail.ru', 'password': 'testtest', 'password_confirm': 'testtest'}
    
    async def mock_get_user(session: AsyncSession, email: EmailStr) -> None:
        return None
 
    monkeypatch.setattr(crud, 'get_user', mock_get_user)
    
    async def mock_create_user(session: AsyncSession, user: schemas.CreateUser) -> models.User:
        return models.User(email=user.email, hashed_password='testtest')
 
    monkeypatch.setattr(crud, 'create_user', mock_create_user)
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/signup", json=data)
        assert response.status_code == 201
        assert response.json()['email'] == data['email']
        