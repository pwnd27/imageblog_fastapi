from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy import String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


str50 = Annotated[str, 50]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, index=True)]
datetime_now = Annotated[datetime, mapped_column(default=datetime.utcnow)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
    }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    email: Mapped[str50]
    hashed_password: Mapped[str50]


# class Profile(Base):
#     pass


# class Image(Base):
#     pass

