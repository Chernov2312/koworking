__all__ = ()
import uuid
from datetime import datetime
from functools import wraps

from sqlalchemy import UUID, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from config.settings import settings

engine = create_async_engine(url=settings.get_db_url)
postgres_session_maker = async_sessionmaker(engine, expire_on_commit=False)

current_session_maker = postgres_session_maker


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


def connection(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        if 'session' in kwargs:
            return await method(*args, **kwargs)

        async with current_session_maker() as session:
            try:
                kwargs['session'] = session
                result = await method(*args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e

    return wrapper


async def get_session() -> AsyncSession:
    async with postgres_session_maker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
