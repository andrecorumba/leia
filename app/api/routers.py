from fastapi import APIRouter

_routers = APIRouter()

@_routers.get("/items/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]
