from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from app.api.routes import users, auth
from app.oauth2 import Settings


app = FastAPI()


@AuthJWT.load_config # pyright: ignore
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, # type: ignore
        content={"detail": exc.message} # type: ignore
    )


app.include_router(auth.router, tags=['Users'], prefix='/users')
app.include_router(users.router, tags=['Users'], prefix='/users')
