from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

from app.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


class TestAPI(Base):
    __tablename__ = "test_api"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def populate_test_data():
    async with async_session() as session:
        count = (await session.execute("SELECT COUNT(*) FROM test_api")).scalar()
        if count == 0:
            session.add_all([
                TestAPI(name="Alpha", description="First test record"),
                TestAPI(name="Beta", description="Second test record"),
                TestAPI(name="Gamma", description="Third test record"),
            ])
            await session.commit()
            print("✅ Added sample test data.")
        else:
            print("ℹ️ Table already has data.")
