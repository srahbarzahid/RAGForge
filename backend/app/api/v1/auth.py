"""Supabase-authenticated identity endpoint."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import current_user_claims

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthMe(BaseModel):
    user_id: UUID
    email: str | None = None


@router.get("/me", response_model=AuthMe)
def me(claims: Annotated[dict, Depends(current_user_claims)]) -> AuthMe:
    return AuthMe(user_id=claims["sub"], email=claims.get("email"))
