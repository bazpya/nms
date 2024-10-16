from fastapi import FastAPI
from engine.router import Router

app = FastAPI()


@app.get("/")
async def get_root() -> str:
    message = """To try this API using Swagger UI browse /docs.
    To see its interface definition browse /redoc"""
    return message


# ==========================  Query  ==========================


@app.get("/{id}/interfaces")
async def get_interfaces(id: int) -> list[str]:
    router = Router(id)
    interface_names = router.list_interfaces(loopback_only=False)
    return interface_names


@app.get("/{id}/interfaces/loopback")
async def get_interfaces_loopback(id: int) -> list[str]:
    router = Router(id)
    interface_names = router.list_interfaces(loopback_only=True)
    return interface_names


# ==========================  Command  ==========================


@app.post("/{id}/interfaces/loopback")
async def post_interfaces_loopback(id: int) -> int:
    router = Router(id)
    loopback_suffix_added = router.add_loopback()
    return loopback_suffix_added


@app.delete("/{id}/interfaces/loopback/{suffix}")
async def delete_interfaces_loopback(id: int, suffix: int) -> list[int]:
    router = Router(id)
    remaining_suffixes = router.delete_loopback(suffix)
    return remaining_suffixes
