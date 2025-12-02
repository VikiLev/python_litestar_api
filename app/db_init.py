import asyncio
from sqlalchemy.exc import OperationalError
from app.models import Base
from app.database import engine
from app.models import TestAPI
from sqlalchemy import select


RETRY_INTERVAL = 2
MAX_RETRIES = 10


async def seed_data():
    from app.database import async_session
    
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(TestAPI))
            existing = result.scalars().first()
            if not existing:
                session.add_all(
                    [
                        TestAPI(name="Test 1", description="First test"),
                        TestAPI(name="Test 2", description="Second test"),
                    ]
                )
        await session.commit()


async def init_db():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ The database is ready and the tables have been created")

            await seed_data()
            print("✅ Seed data has been added")

            return
        except OperationalError:
            retries += 1
            print(f"⚠️ Сouldn't connect to the database. Try {retries}/{MAX_RETRIES}...")
            await asyncio.sleep(RETRY_INTERVAL)
    raise RuntimeError(" Couldn't connect to the database after many tries")


if __name__ == "__main__":
    asyncio.run(init_db())
