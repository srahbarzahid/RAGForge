"""SQLAlchemy connection factory for the hosted Supabase PostgreSQL database."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    settings = get_settings()
    database_url = settings.database_url
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    if database_url.startswith("postgres://"):
        database_url = "postgresql+psycopg://" + database_url[len("postgres://") :]
    elif database_url.startswith("postgresql://"):
        database_url = "postgresql+psycopg://" + database_url[len("postgresql://") :]
    elif not database_url.startswith("postgresql+psycopg://"):
        raise RuntimeError("DATABASE_URL must use PostgreSQL")
    ssl_args = {"sslmode": "require"}
    if settings.database_ssl_root_cert:
        ssl_args = {
            "sslmode": "verify-full",
            "sslrootcert": settings.database_ssl_root_cert,
        }
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args=ssl_args,
    )


def get_db() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
