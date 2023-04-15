from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_hashed_password
from app.api import models


async def get_user(email: str, session: AsyncSession) -> models.User | None:
    return await session.scalar(select(models.User).where(models.User.email == email))
    

async def create_user(user: dict, session: AsyncSession) -> models.User:
    hashed_password = await get_hashed_password(user['password'])
    db_user = models.User(email=user['email'], hashed_password=hashed_password)
    session.add(db_user)
    await session.flush()
    return db_user
