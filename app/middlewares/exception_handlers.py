from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"message": exc.detail}
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP error",
            "status_code": exc.status_code,
            "message": detail.get("message", "Ha ocurrido un error")
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [
        {
            "field": error["loc"][-1],
            "message": error["msg"]
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Erro de validacion",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Los datos de la solicitud no son válidos.",
            "details": error_messages
        }
    )