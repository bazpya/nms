from typing import Any, Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class Status(BaseModel):
    code: int
    message: str


class Error(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Any] = None


class Response(BaseModel):
    status: Status
    data: Optional[Any] = None
    error: Optional[Error] = None


class ResponseFactory:

    def make_success(
        data: Any,
        message: str = "Success",
        code: int = 200,
    ):
        return JSONResponse(
            status_code=code,
            content={
                "status": {"code": code, "message": message},
                "data": data,
                "error": None,
            },
        )

    def make_error(
        error_code: int,
        error_message: str,
        details: Any = None,
        http_status_code: int = 400,
    ):
        return JSONResponse(
            status_code=http_status_code,
            content={
                "status": {"code": error_code, "message": error_message},
                "data": None,
                "error": {
                    "code": str(error_code),
                    "message": error_message,
                    "details": details,
                },
            },
        )
