from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from utils import get_hashed_password

import schemas
import models


async def get_user(session: AsyncSession, email: EmailStr) -> models.User:
    return await session.scalar(select(models.User).where(models.User.email == email))
    

async def create_user(session: AsyncSession, user: schemas.CreateUser) -> models.User:
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    await session.flush()
    return db_user
