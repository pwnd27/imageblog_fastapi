import pytest
from sqlalchemy.exc import IntegrityError
from app.api import service


@pytest.mark.asyncio
async def test_get_user_when_exist_in_db(session, user) -> None:
    email = 'test@mail.ru'    
    user = await service.get_user(email=email, session=session)
    assert user != None
    assert email == user.email
    
    
@pytest.mark.asyncio
async def test_get_user_when_not_exist_in_db(session) -> None:
    email = 'testtest@mail.ru'
    user = await service.get_user(email=email, session=session)
    assert user == None
    
    
@pytest.mark.asyncio
async def test_create_user_when_not_exist_in_db(session) -> None:
    user_data = {'email': 'test2@mail.ru', 'password': 'test_password'}
    user = await service.create_user(user=user_data, session=session)
    assert user.email == user_data['email']
    
    
@pytest.mark.asyncio
@pytest.mark.xfail(raises=IntegrityError)
async def test_create_user_when_exist_in_db(session, user) -> None:
    user_data = {'email': user.email, 'password': user.hashed_password}
    await service.create_user(user=user_data, session=session)
    