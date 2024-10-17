from fastapi import FastAPI, Path
from fastapi.responses import RedirectResponse
from engine.router import Router
from api.text_repository import descriptions, app_description, summaries, tags_metadata
from api.response_factory import ResponseFactory, Response, Error

app = FastAPI(**app_description)


# ==========================  Query  ==========================


@app.get("/", summary=summaries["get_root"])
async def get_root() -> str:
    response = RedirectResponse(url="/docs")
    return response


@app.get(
    "/{id}/interfaces",
    response_model=Response,
    summary=summaries["get_interfaces"],
)
async def get_interfaces(
    id: int = Path(..., description=descriptions["id"])
) -> Response:
    router = Router(id)
    try:
        interface_names = router.list_interfaces(loopback_only=False)
        return ResponseFactory.make_success(
            data=interface_names,
            message="List of all interfaces on the router",
        )
    except:
        return ResponseFactory.make_error(
            error_code=404,
            error_message="failed",
        )


@app.get(
    "/{id}/interfaces/loopback",
    response_model=Response,
    summary=summaries["get_interfaces_loopback"],
)
async def get_interfaces_loopback(
    id: int = Path(..., description=descriptions["id"])
) -> Response:
    router = Router(id)
    try:
        interface_names = router.list_interfaces(loopback_only=True)
        return ResponseFactory.make_success(
            data=interface_names,
            message="List of only loopback interfaces on the router",
        )
    except:
        return ResponseFactory.make_error(
            error_code=404,
            error_message="failed",
        )


# ==========================  Command  ==========================


@app.post(
    "/{id}/interfaces/loopback",
    response_model=Response,
    summary=summaries["post_interfaces_loopback"],
)
async def put_interfaces_loopback(
    id: int = Path(..., description=descriptions["id"])
) -> Response:
    router = Router(id)
    try:
        loopback_suffix_added = router.add_loopback()
        return ResponseFactory.make_success(
            code=201,
            data=loopback_suffix_added,
            message="Numerical suffix of the newly added loopback",
        )
    except:
        return ResponseFactory.make_error(
            error_code=404,
            error_message="failed",
        )


@app.delete(
    "/{id}/interfaces/loopback/{suffix}",
    response_model=Response,
    summary=summaries["delete_interfaces_loopback"],
)
async def delete_interfaces_loopback(
    id: int = Path(..., description=descriptions["id"]),
    suffix: int = Path(..., description=descriptions["suffix"]),
) -> Response:
    router = Router(id)
    try:
        remaining_suffixes = router.delete_loopback(suffix)
        return ResponseFactory.make_success(
            code=204,
            data=remaining_suffixes,
            message="Numerical suffixes of remaining loopback interfaces",
        )
    except:
        return ResponseFactory.make_error(
            error_code=404,
            error_message="failed",
        )
