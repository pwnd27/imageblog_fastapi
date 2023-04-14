from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from app.routers.users import users


app = FastAPI()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, # type: ignore
        content={"detail": exc.message} # type: ignore
    )


app.include_router(users.router, tags=['Users'], prefix='/users')
