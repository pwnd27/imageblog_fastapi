from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUser(User):
    password: constr(min_length=8) # pyright: ignore
    password_confirm: str


class LoginUser(User):
    password: constr(min_length=8) # pyright: ignore
