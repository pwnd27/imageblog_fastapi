from fastapi import FastAPI
from app.routers import users
from app import schemas

app = FastAPI()
app.include_router(users.router, tags=['Users'], prefix='/users')
