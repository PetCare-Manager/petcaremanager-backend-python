"""
PetCareManager Backend built FastAPI 
"""

from fastapi import FastAPI
from config.database import engine, Base
from middlewares.cors import setup_cors
from routers.user import user_router
from routers.password import pass_router


app = FastAPI(
    title="PetCare Manager",
    description="Manage your pets schedules, appointments, medicine",
    version="0.0.1",
)
setup_cors(app)

app.include_router(user_router, prefix="/api")
app.include_router(pass_router, prefix="/api/auth/password", tags=["Auth"])

@app.get("/health", tags=["Health"])
def health_check():
    """Health Check"""
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)
