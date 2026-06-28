__all__ = ()
from typing import AsyncGenerator

import httpx
import pytest
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import db.database as db_module
from config.db import seed_initial_data
from db.database import Base, get_session

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
engine_test = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={'check_same_thread': False},
)
sqlite_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest.fixture(scope='function', autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db_module.current_session_maker = sqlite_session_maker

    await seed_initial_data()

    yield

    db_module.current_session_maker = db_module.postgres_session_maker

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sqlite_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='function')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        yield client
