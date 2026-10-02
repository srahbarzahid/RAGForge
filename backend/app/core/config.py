"""Environment configuration shared by backend integrations."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")


@dataclass(frozen=True)
class Settings:
    supabase_url: str | None
    database_url: str | None
    database_ssl_root_cert: str | None
    frontend_origin: str


def get_settings() -> Settings:
    return Settings(
        supabase_url=os.getenv("SUPABASE_URL", "").rstrip("/") or None,
        database_url=os.getenv("DATABASE_URL") or None,
        database_ssl_root_cert=os.getenv("DATABASE_SSL_ROOT_CERT") or None,
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
    )
