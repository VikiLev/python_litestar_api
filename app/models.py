import asyncio
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import Integer, String, select
from sqlalchemy.exc import IntegrityError
from app.config import settings

class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine(settings.DB_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class TestAPI(Base):
    __tablename__ = "test_api"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

async def seed_data():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(TestAPI))
            existing = result.scalars().first()
            if not existing:
                session.add_all([
                    TestAPI(name="Test 1", description="First test"),
                    TestAPI(name="Test 2", description="Second test"),
                ])
        await session.commit()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()


if __name__ == "__main__":
    asyncio.run(init_db())

