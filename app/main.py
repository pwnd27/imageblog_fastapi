from fastapi import FastAPI
from app.routers import users
from app import schemas

app = FastAPI()
app.include_router(users.router, tags=['Users'], prefix='/users')


@app.get('/')
async def root():
    return {'message': 'Hello friend!'}


@app.post('/')
async def postroot(user: schemas.UserBase):
    return user