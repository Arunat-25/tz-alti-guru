from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(url=settings.DATABASE_URL)
session_factory = async_sessionmaker(engine)


async def get_session():
    async with session_factory() as session:
        yield session
