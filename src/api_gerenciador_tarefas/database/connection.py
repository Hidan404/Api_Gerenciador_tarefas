from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


#DATABASE_URL = "postgresql://ronald:new@127.0.0.1:5433/tasks_db"

DATABASE_URL = "postgresql+asyncpg://ronald:new@127.0.0.1:5433/tasks_db"


engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_session():
    async with SessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass