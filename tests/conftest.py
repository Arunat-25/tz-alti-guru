import pytest
import sqlalchemy as sa
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from src.database.session import get_session
from src.main import app


@pytest.fixture(scope="function")
async def db_session():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        await session.begin()
        try:
            yield session
        finally:
            if session.is_active:
                try:
                    await session.rollback()
                except sa.exc.ResourceClosedError:
                    pass  # Транзакция уже закрыта
            await session.close()

    await engine.dispose()


@pytest.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
