# Module 2 — Relational schema and migrations

## Live schema

Alembic revisions `20261002_01` and `20261002_02` create the eight tables in the database plan: `profiles`, `knowledge_bases`, `documents`, `conversations`, `messages`, `feedback`, `usage_records`, and `audit_logs`. Supabase continues to own `auth.users`. The migration also creates `alembic_version`. All nine public tables have RLS enabled.

The tables use UUID keys, timestamps, nonnegative counts/costs, document lifecycle states, and indexes on owner and foreign-key columns. Composite foreign keys prevent a document from linking to another user's knowledge base, a conversation from linking to another user's knowledge base, a message from linking to another user's conversation, and feedback from linking to another user's message. `messages.user_id` is an extra ownership column needed for those constraints.

## Access boundary

`anon` and `authenticated` have no direct table privileges. There are no direct-client policies. Supabase's [`rls_enabled_no_policy` INFO notice](https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy) is expected for this closed design; it does not grant access. FastAPI is the planned path for user-owned application workflows and must check ownership on every operation because its database role is privileged. Prisma mirrors the eight models for server-side use, while Alembic owns schema changes. Do not use Prisma Migrate or expose the database URL to browser code.

The database clients require encrypted TLS connections to the Session pooler. Without a CA file they use `sslmode=require`, which does not verify the server certificate. Set `DATABASE_SSL_ROOT_CERT` to the project's downloaded CA certificate path in both server environments to switch to `verify-full`. [Supabase recommends this mode](https://supabase.com/docs/guides/database/connecting-to-postgres) for production use. Keep the CA and database credentials in server environments. Do not set `NEXT_PUBLIC_DATABASE_URL`.

## Apply and verify

From `backend`:

```powershell
.venv/Scripts/alembic.exe upgrade head
.venv/Scripts/alembic.exe check
.venv/Scripts/python.exe -m scripts.check_schema
.venv/Scripts/python.exe -m scripts.check_database
```

From `frontend`:

```powershell
npm.cmd run db:generate
npm.cmd run db:check
```

The schema check verifies the eight application tables, RLS, closed grants, composite ownership foreign keys, and migration revision without writing data. Prisma's check reads all eight tables. The hosted schema had zero application rows and zero Auth users immediately after migration; no test user was created for this work.

## Scaffold review

The required top-level and module directories from `02_PROJECT_SCAFFOLD.md` exist. The scaffold document was renamed to match the execution plan's reference. Module 2 adds SQLAlchemy models, Alembic migrations, and a Prisma model mirror. Later module routes, services, workers, and frontend pages remain directory placeholders according to the execution sequence; the full product workflow is not implemented by this schema migration.
