"""
PetCareManager Backend built with FastAPI 
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from config.database import engine, Base
from middlewares.cors import setup_cors
from middlewares.error_handler import ErrorHandler
from middlewares.exception_handlers import http_exception_handler, validation_exception_handler
from routers.user import user_router
from routers.password import pass_router
from routers.pet import pet_router

app = FastAPI(
    title="PetCare Manager",
    description="Manage your pets schedules, appointments, medicine",
    version="0.0.1",
)

setup_cors(app)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(ErrorHandler)

app.include_router(user_router, prefix="/api")
app.include_router(pass_router, prefix="/api/auth/password", tags=["Auth"])
app.include_router(pet_router, prefix="/api/pets", tags=["Pets"])

@app.get("/health", tags=["Health"])
def health_check():
    """Health Check"""
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)
