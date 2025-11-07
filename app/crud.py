from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import TestAPI, async_session
import logging

logger = logging.getLogger(__name__)


# GET all
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


# GET by ID
async def get_test_by_id(test_id: int) -> dict | None:
    try:
        async with async_session() as session:
            result = await session.execute(select(TestAPI).where(TestAPI.id == test_id))
            test = result.scalar_one_or_none()
            if test:
                return {
                    "id": test.id,
                    "name": test.name,
                    "description": test.description
                }
            return None
    except Exception as e:
        logger.exception(f"Error retrieving test with id={test_id}")
        raise

async def create_test(name: str, description: str | None = None) -> dict:
    async with async_session() as session:
        new_test = TestAPI(name=name, description=description)
        session.add(new_test)
        await session.commit()
        await session.refresh(new_test)
        return {
            "id": new_test.id,
            "name": new_test.name,
            "description": new_test.description,
        }


# UPDATE
async def update_test(test_id: int, name: str | None = None, description: str | None = None) -> dict | None:
    async with async_session() as session:
        test = await session.get(TestAPI, test_id)
        if not test:
            return None
        if name:
            test.name = name
        if description is not None:
            test.description = description
        await session.commit()
        await session.refresh(test)
        return {"id": test.id, "name": test.name, "description": test.description}

# DELETE
async def delete_test(test_id: int) -> bool:
    async with async_session() as session:
        test = await session.get(TestAPI, test_id)
        if not test:
            return False
        await session.delete(test)
        await session.commit()
        return True