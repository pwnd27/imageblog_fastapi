from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
)


str50 = Annotated[str, 50]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, index=True)]
timestamp = Annotated[datetime, mapped_column(default=func.now())]


class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
        timestamp: TIMESTAMP(timezone=True),
    }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    email: Mapped[str50]
    hashed_password: Mapped[str50]

    def __repr__(self) -> str:
        return f'User(id={self.id}, email={self.email})'


# class Profile(Base):
#     pass


# class Image(Base):
#     pass

