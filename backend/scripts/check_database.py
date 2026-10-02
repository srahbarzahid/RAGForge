"""Read-only connectivity check for the configured Supabase PostgreSQL URL."""

from sqlalchemy import text

from app.infrastructure.database.session import get_engine


def main() -> None:
    with get_engine().connect() as connection:
        if connection.execute(text("SELECT 1")).scalar_one() != 1:
            raise RuntimeError("Database did not answer the connectivity check")
    print("Supabase PostgreSQL connection OK")


if __name__ == "__main__":
    main()
