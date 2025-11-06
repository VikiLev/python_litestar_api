from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import TestAPI, async_session
import logging

logger = logging.getLogger(__name__)

async def get_all_tests() -> list[dict]:
    try:
        async with async_session() as session:
            result = await session.execute(select(TestAPI))
            tests = result.scalars().all()
            return [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description
                } for t in tests
            ]
    except Exception as e:
        logger.exception("Error retrieving tests from the database")
        raise
