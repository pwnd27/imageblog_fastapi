import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Base, User


# @pytest.fixture(scope='function')
# async def db_session():

#     engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     async_session = sessionmaker(
#         engine, expire_on_commit=False, class_=AsyncSession
#     )

#     async with async_session() as session:
#         yield session

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope='function')
# async def user(db_session):
#     user = User(email='test@mail.ru', hashed_password='qwerty123')
#     db_session.add(user)
#     await db_session.flush()
#     return user
