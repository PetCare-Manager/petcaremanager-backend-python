"""
CORS Middleware Configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI) -> None:
    """
    Sets up CORS middleware for the FastAPI application.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Puedes especificar orígenes específicos en lugar de "*"
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
