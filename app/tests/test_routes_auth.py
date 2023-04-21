# import pytest
# from app.api import service
# from app.api import models


# @pytest.mark.asyncio
# async def test_register_should_return_error_400_when_user_exist(monkeypatch, client) -> None:
#     data = {'email': 'test12@mail.ru', 'password': 'testtest', 'password_confirm': 'testtest'}
 
#     async def mock_get_user(email, session) -> models.User:
#         return models.User(email='test12@mail.ru', hashed_password='testtest')
 
#     monkeypatch.setattr(service, 'get_user', mock_get_user)

#     response = await client.post("/users/signup", json=data)
#     assert response.status_code == 400


# @pytest.mark.asyncio
# async def test_register_when_not_exist_in_db(monkeypatch, client) -> None:
#     data = {'email': 'test12@mail.ru', 'password': 'testtest', 'password_confirm': 'testtest'}
    
#     async def mock_get_user(email, session) -> None:
#         return None
 
#     monkeypatch.setattr(service, 'get_user', mock_get_user)
    
#     async def mock_create_user(user, session) -> models.User:
#         return models.User(email=user.email, hashed_password='testtest')
 
#     monkeypatch.setattr(service, 'create_user', mock_create_user)

#     response = await client.post("/users/signup", json=data)
#     assert response.status_code == 201
#     assert response.json()['email'] == data['email']
        