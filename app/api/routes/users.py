from typing import Annotated, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.api import crud, schemas
from app import oauth2


async_session = Annotated[AsyncSession, Depends(get_session)]
user_email = Annotated[str, Depends(oauth2.current_user)]


router = APIRouter()


@router.get('/me', response_model=schemas.User)
async def get_current_user(session: async_session, email: user_email) -> Any:
    return await crud.get_user(email=email, session=session)
