"""
JWTBearer class for handling authentication using JSON Web Tokens (JWT).

This class extends FastAPI's HTTPBearer to implement token-based authentication.
It verifies the presence and validity of a JWT token in the Authorization header
of incoming requests.
"""
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    """
    Methods:
        __call__: Overrides the parent class method to validate the JWT token.
            Raises an HTTPException if the token is invalid, expired, or missing.

    Usage:
        Use JWTBearer as a dependency in FastAPI routes to protect endpoints that
        require authentication. The token must be provided in the format:
        "Authorization: Bearer <token>".

    Raises:
        HTTPException: If the token is missing, invalid, or expired, with a status code of 403.
    """
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        # Ensure token exists
        if not auth or not auth.credentials:
            raise HTTPException(status_code=403, detail="Invalid or missing credentials")
        try:
            data = validate_token(auth.credentials)
            email = data.get("email")
            user_id = data.get("user_id")
            if not email or not user_id:
                raise HTTPException(status_code=403, detail="Invalid credentials")
            request.state.email = email
            request.state.user_id = user_id
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e)) from e
