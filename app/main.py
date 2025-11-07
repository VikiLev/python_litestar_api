from litestar import Litestar
from app.routes import (
    list_tests,
    health_check,
    retrieve_test,
    create_test,
    update_test,
    delete_test,
)
from app.db_init import init_db
import asyncio

litestar_app = Litestar(
    route_handlers=[
        list_tests,
        health_check,
        retrieve_test,
        create_test,
        update_test,
        delete_test,
    ],
    debug=True,
)


async def asgi_app(scope, receive, send):
    await init_db()
    await litestar_app(scope, receive, send)
