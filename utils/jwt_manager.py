"""
JWT Manager for creating and validating JSON Web Tokens.
SECRET_KEY from ENV
"""

import os
from typing import Dict
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError # type: ignore
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "my_default_secret_key")

def create_token(data: Dict[str, str]) -> str:
    """Creates a JWT token from the provided data."""
    token: str = encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token: str) -> Dict[str, str]:
    """Validates the JWT token and returns the decoded data."""
    try:
        data: Dict[str, str] = decode(token, key=SECRET_KEY, algorithms=["HS256"])
        return data
    except ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc
