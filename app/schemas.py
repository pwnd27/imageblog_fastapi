from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: constr(min_length=8)
    password_confirm: str


class LoginUser(UserBase):
    password: constr(min_length=8)
