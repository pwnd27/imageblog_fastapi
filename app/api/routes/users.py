from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from app.api import schemas


authjwt = Annotated[AuthJWT, Depends()]

router = APIRouter()


@router.get('/me')
async def current_user(authorize: authjwt) -> Any:
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    return {'user': current_user}
