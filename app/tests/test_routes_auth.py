import pytest
from httpx import Cookies
from fastapi import status
from app.api import service
from app.api import models


@pytest.mark.asyncio
async def test_register_should_return_error_409_when_user_exist(monkeypatch, client) -> None:
    data = {
        'email': 'test@mail.ru', 
        'password': 'testtest', 
        'password_confirm': 'testtest'
    }
 
    async def mock_get_user(email, session) -> models.User:
        return models.User(email=data['email'], hashed_password=data['password'])
    monkeypatch.setattr(service, 'get_user', mock_get_user)

    response = await client.post('/auth/signup', json=data)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_register_when_not_exist_in_db(monkeypatch, client) -> None:
    data = {
        'email': 'test12@mail.ru', 
        'password': 'testtest', 
        'password_confirm': 'testtest'
    }
    
    async def mock_get_user(email, session) -> None:
        return None
    monkeypatch.setattr(service, 'get_user', mock_get_user)
    
    async def mock_create_user(user, session) -> models.User:
        return models.User(email=data['email'], hashed_password=data['password'])
    monkeypatch.setattr(service, 'create_user', mock_create_user)

    response = await client.post('/auth/signup', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['email'] == data['email']
    

@pytest.mark.asyncio
async def test_register_when_passwords_no_match(client) -> None:
    data = {
        'email': 'test12@mail.ru', 
        'password': 'testtest', 
        'password_confirm': 'test'
    }
    
    response = await client.post('/auth/signup', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Пароли не совпадают'
    
        
@pytest.mark.asyncio
async def test_login_when_user_not_exist_in_db(monkeypatch, client) -> None:
    data = {'email': 'test@mail.ru', 'password': 'testtest'}
    
    async def mock_get_user(email, session) -> None:
        return None
    monkeypatch.setattr(service, 'get_user', mock_get_user)
    
    response = await client.post('/auth/login', json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Неверная почта или пароль'
    assert response.headers.get('set-cookie') == None
    
    
@pytest.mark.asyncio
async def test_login_when_user_is_exist_but_wrong_pass(monkeypatch, client, user) -> None:
    data = {'email': 'test@mail.ru', 'password': 'test_wrong_pass'}
    
    async def mock_get_user(email, session) -> models.User:
        return models.User(email=user.email, hashed_password=user.hashed_password)
    monkeypatch.setattr(service, 'get_user', mock_get_user)
    
    response = await client.post('/auth/login', json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Неверная почта или пароль'
    assert response.headers.get('set-cookie') == None
    
    
@pytest.mark.asyncio
async def test_login_when_user_is_exist_success_sign_in(monkeypatch, client, user) -> None:
    data = {'email': 'test@mail.ru', 'password': 'qwerty123'}
    
    async def mock_get_user(email, session) -> models.User:
        return models.User(email=user.email, hashed_password=user.hashed_password)
    monkeypatch.setattr(service, 'get_user', mock_get_user)
    
    response = await client.post('/auth/login', json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['msg'] == 'Успешный вход в систему'
    assert response.headers.get('set-cookie') != None
    
    
@pytest.mark.asyncio
async def test_refresh_with_cookie(user_cookies, client) -> None:
    response = await client.get('/auth/refresh', cookies=user_cookies)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['msg'] == 'Токен обновлен'
    
    
@pytest.mark.asyncio
async def test_refresh_without_cookie(client) -> None:
    response = await client.get('/auth/refresh')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Missing cookie refresh_token_cookie'

    
@pytest.mark.asyncio
async def test_logout_with_cookie(user_cookies, client) -> None:
    response = await client.get('/auth/logout', cookies=user_cookies)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['msg'] == 'Успешный выход из системы'
    