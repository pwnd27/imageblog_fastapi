from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./imageblog.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

