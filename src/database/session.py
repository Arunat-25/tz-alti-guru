from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url="postgresql+asyncpg://admin:secret@database:5432/marketplace")
session_factory = async_sessionmaker(engine)


async def get_session():
    async with session_factory() as session:
        yield session
