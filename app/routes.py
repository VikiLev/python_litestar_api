from litestar import get
from app.crud import get_all_tests

@get("/tests")
async def list_tests() -> list[dict]:
    return await get_all_tests()

@get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
