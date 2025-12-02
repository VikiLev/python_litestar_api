from litestar import get, post, put, delete, Provide
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import (
    get_all_tests,
    get_test_by_id as crud_get_test_by_id,
    create_test as crud_create_test,
    update_test as crud_update_test,
    delete_test as crud_delete_test,
)
from app.schemas import (
    TestResponseSchema,
    CreateTestSchema,
    UpdateTestSchema,
)
from app.dependencies import provide_session


@get("/tests", dependencies={"session": Provide(provide_session)})
async def list_tests(session: AsyncSession) -> list[TestResponseSchema]:
    tests = await get_all_tests(session)
    return [TestResponseSchema(**test) for test in tests]


@get("/tests/{test_id:int}", dependencies={"session": Provide(provide_session)})
async def retrieve_test(test_id: int, session: AsyncSession) -> TestResponseSchema:
    test = await crud_get_test_by_id(test_id, session)
    if test is None:
        raise HTTPException(status_code=404, detail=f"Test with id={test_id} not found")
    return TestResponseSchema(**test)


@post("/tests", dependencies={"session": Provide(provide_session)})
async def create_test(data: CreateTestSchema, session: AsyncSession) -> TestResponseSchema:
    new_test = await crud_create_test(
        name=data.name,
        description=data.description,
        session=session
    )
    return TestResponseSchema(**new_test)


@put("/tests/{test_id:int}", dependencies={"session": Provide(provide_session)})
async def update_test(
    test_id: int,
    data: UpdateTestSchema,
    session: AsyncSession
) -> TestResponseSchema:
    updated = await crud_update_test(
        test_id,
        session=session,
        name=data.name,
        description=data.description
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Test not found")
    return TestResponseSchema(**updated)


@delete("/tests/{test_id:int}", status_code=200, dependencies={"session": Provide(provide_session)})
async def delete_test(test_id: int, session: AsyncSession) -> dict:
    deleted = await crud_delete_test(test_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"status": "deleted", "id": test_id}


@get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
