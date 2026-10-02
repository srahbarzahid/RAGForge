"""Verify Supabase access tokens using the project's public signing keys."""

from functools import lru_cache
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient
from jwt.exceptions import (
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)

from app.core.config import get_settings


@lru_cache(maxsize=8)
def _jwks_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url, lifespan=300)


def verify_supabase_token(token: str) -> dict:
    project_url = get_settings().supabase_url
    if not project_url or not project_url.startswith("https://"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase Auth is not configured",
        )

    issuer = f"{project_url}/auth/v1"
    try:
        signing_key = _jwks_client(
            f"{issuer}/.well-known/jwks.json"
        ).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=issuer,
            options={"require": ["exp", "sub", "iss", "aud"]},
        )
        UUID(claims["sub"])
        if claims.get("role") != "authenticated":
            raise InvalidTokenError("Unexpected role")
        return claims
    except PyJWKClientConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase signing keys are unavailable",
        ) from exc
    except (InvalidTokenError, PyJWKClientError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
