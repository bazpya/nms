from fastapi import FastAPI, Path
from fastapi.responses import RedirectResponse
from engine.router import Router
from api.text_repository import descriptions, app_description, summaries, tags_metadata

app = FastAPI(**app_description)


# ==========================  Query  ==========================


@app.get("/", summary=summaries["get_root"])
async def get_root() -> str:
    response = RedirectResponse(url="/docs")
    return response


@app.get("/{id}/interfaces", summary=summaries["get_interfaces"])
async def get_interfaces(
    id: int = Path(..., description=descriptions["id"])
) -> list[str]:
    router = Router(id)
    interface_names = router.list_interfaces(loopback_only=False)
    return interface_names


@app.get("/{id}/interfaces/loopback", summary=summaries["get_interfaces_loopback"])
async def get_interfaces_loopback(
    id: int = Path(..., description=descriptions["id"])
) -> list[str]:
    router = Router(id)
    interface_names = router.list_interfaces(loopback_only=True)
    return interface_names


# ==========================  Command  ==========================


@app.post("/{id}/interfaces/loopback", summary=summaries["post_interfaces_loopback"])
async def post_interfaces_loopback(
    id: int = Path(..., description=descriptions["id"])
) -> int:
    router = Router(id)
    loopback_suffix_added = router.add_loopback()
    return loopback_suffix_added


@app.delete(
    "/{id}/interfaces/loopback/{suffix}",
    summary=summaries["delete_interfaces_loopback"],
)
async def delete_interfaces_loopback(id: int, suffix: int) -> list[int]:
    router = Router(id)
    remaining_suffixes = router.delete_loopback(suffix)
    return remaining_suffixes
