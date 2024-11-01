"""
PetCareManager Backend built FastAPI 
"""

from fastapi import FastAPI
from config.database import engine, Base
from routers.user import user_router


app = FastAPI(
    title="PetCare Manager",
    description="Manage your pets schedules, appointments, medicine",
    version="0.0.1",
)
app.include_router(user_router, prefix="/api")

@app.get("/")
def read_root():
    """Root directory"""
    return {"message": "Welcome to PetCareManager Backend"}

@app.get("/health", tags=["Health"])
def health_check():
    """Health Check"""
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)
