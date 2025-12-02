from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session


async def provide_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для отримання сесії БД через Litestar DI"""
    async with async_session() as session:
        yield session
