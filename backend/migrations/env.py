"""Run application migrations using the configured Supabase connection."""

from alembic import context

from app.infrastructure.database.models import Base
from app.infrastructure.database.session import get_engine

target_metadata = Base.metadata


def include_object(object_, name, type_, reflected, compare_to):
    return not (
        type_ == "table" and (name == "alembic_version" or object_.info.get("external"))
    )


def run_migrations_online() -> None:
    with get_engine().connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="public",
            compare_type=True,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError("Use a live connection for RAGForge migrations")
run_migrations_online()
