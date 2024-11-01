"""
ErrorHandler Middleware

This middleware handles unexpected exceptions in the FastAPI application.
"""

from typing import Awaitable, Callable, Union
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandler(BaseHTTPMiddleware):
    """
    This middleware handles unexpected exceptions in the FastAPI application.
    """
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Union[Response, JSONResponse]:
        try:
            return await call_next(request)
        except (TypeError, ValueError, KeyError, AttributeError) as e:
            return JSONResponse(status_code=400, content={
                "error": "Invalid request data", 
                "message": str(e)
            })
        except (IntegrityError, OperationalError, DataError) as e:
            return JSONResponse(status_code=500, content={
                "error": "Database error",
                "message": str(e)
            })
