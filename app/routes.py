from litestar import get, post, put, delete, Request
from litestar.exceptions import HTTPException
from app.crud import (
    get_all_tests,
    get_test_by_id as crud_get_test_by_id,
    create_test as crud_create_test,
    update_test as crud_update_test,
    delete_test as crud_delete_test
)

@get("/tests")
async def list_tests() -> list[dict]:
    return await get_all_tests()


@get("/tests/{test_id:int}")
async def retrieve_test(test_id: int) -> dict | None:
    test = await crud_get_test_by_id(test_id)
    if test is None:
        raise HTTPException(status_code=404, detail=f"Test with id={test_id} not found")
    return test


@post("/tests")
async def create_test(request: Request) -> dict:
    data = await request.json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        raise HTTPException(status_code=400, detail="Field 'name' is required")

    new_test = await crud_create_test(name=name, description=description)
    return new_test


@put("/tests/{test_id:int}")
async def update_test(test_id: int, request: Request) -> dict:
    data = await request.json()
    name = data.get("name")
    description = data.get("description")

    updated = await crud_update_test(test_id, name=name, description=description)
    if not updated:
        raise HTTPException(status_code=404, detail="Test not found")
    return updated


@delete("/tests/{test_id:int}", status_code=200)
async def delete_test(test_id: int) -> dict:
    deleted = await crud_delete_test(test_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"status": "deleted", "id": test_id}


@get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
