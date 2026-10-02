"""Read-only audit of Module 2 tables, access grants, and migration state."""

from sqlalchemy import text

from app.infrastructure.database.session import get_engine

TABLES = {
    "profiles",
    "knowledge_bases",
    "documents",
    "conversations",
    "messages",
    "feedback",
    "usage_records",
    "audit_logs",
}

OWNERSHIP_FOREIGN_KEYS = {
    "documents_knowledge_base_id_user_id_fkey",
    "conversations_knowledge_base_id_user_id_fkey",
    "messages_conversation_id_user_id_fkey",
    "feedback_message_id_user_id_fkey",
}


def main() -> None:
    with get_engine().connect() as connection:
        rows = connection.execute(
            text("""
                SELECT tablename, rowsecurity,
                    has_table_privilege('anon', format('public.%I', tablename),
                        'SELECT, INSERT, UPDATE, DELETE') AS anon_access,
                    has_table_privilege('authenticated',
                        format('public.%I', tablename),
                        'SELECT, INSERT, UPDATE, DELETE') AS authenticated_access
                FROM pg_tables WHERE schemaname = 'public'
            """)
        ).mappings()
        tables = {row["tablename"]: row for row in rows}
        missing = TABLES - tables.keys()
        if missing:
            raise RuntimeError(f"Missing application tables: {sorted(missing)}")
        for name in TABLES | {"alembic_version"}:
            row = tables[name]
            if (
                not row["rowsecurity"]
                or row["anon_access"]
                or row["authenticated_access"]
            ):
                raise RuntimeError(f"Unsafe public table permissions: {name}")

        foreign_keys = set(
            connection.execute(
                text("""
                    SELECT conname FROM pg_constraint
                    WHERE contype = 'f' AND connamespace = 'public'::regnamespace
                """)
            ).scalars()
        )
        if not OWNERSHIP_FOREIGN_KEYS <= foreign_keys:
            raise RuntimeError("Missing composite ownership foreign keys")

        revision = connection.execute(
            text("SELECT version_num FROM public.alembic_version")
        ).scalar_one()
        if revision != "20261002_02":
            raise RuntimeError(f"Unexpected database migration revision: {revision}")

    print("Eight application tables, RLS, closed grants, ownership FKs, and Alembic OK")


if __name__ == "__main__":
    main()
