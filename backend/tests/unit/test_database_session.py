"""The database factory must fail closed and use TLS to reach PostgreSQL."""

from unittest.mock import Mock

import pytest

from app.infrastructure.database import session


@pytest.fixture(autouse=True)
def clear_engine_cache():
    session.get_engine.cache_clear()
    yield
    session.get_engine.cache_clear()


def test_database_url_is_required(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL is not configured"):
        session.get_engine()


def test_database_factory_requires_postgresql(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///local.db")
    with pytest.raises(RuntimeError, match="must use PostgreSQL"):
        session.get_engine()


def test_database_factory_normalizes_url_and_requires_tls(monkeypatch):
    monkeypatch.delenv("DATABASE_SSL_ROOT_CERT", raising=False)
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://example:secret@db.example/postgres"
    )
    engine = Mock()
    create_engine = Mock(return_value=engine)
    monkeypatch.setattr(session, "create_engine", create_engine)

    assert session.get_engine() is engine
    assert session.get_engine() is engine
    create_engine.assert_called_once_with(
        "postgresql+psycopg://example:secret@db.example/postgres",
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args={"sslmode": "require"},
    )


def test_database_factory_verifies_host_with_ca(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://example:secret@db.example/postgres"
    )
    monkeypatch.setenv("DATABASE_SSL_ROOT_CERT", "/private/supabase-ca.crt")
    create_engine = Mock()
    monkeypatch.setattr(session, "create_engine", create_engine)

    session.get_engine()

    assert create_engine.call_args.kwargs["connect_args"] == {
        "sslmode": "verify-full",
        "sslrootcert": "/private/supabase-ca.crt",
    }
