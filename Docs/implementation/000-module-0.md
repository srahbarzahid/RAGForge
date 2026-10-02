# Module 0 — architecture review and bootstrap

## Source of truth

The numbered files in `Docs/` describe the product. `07_MODULE_BY_MODULE_EXECUTION_PLAN.md` controls implementation order; `01_FIXED_ARCHITECTURE.md` and `10_FINAL_STACK_AND_DECISIONS.md` freeze the technology choices. This note records the initial review and bootstrap status.

The scaffold drawing uses lowercase `docs/`, but the existing repository uses `Docs/`. Implementation notes live under `Docs/` so the path remains portable across case-sensitive filesystems.

## End-to-end architecture

1. Next.js handles the portal and Supabase Auth session. It sends the user's Supabase JWT to FastAPI over REST, using SSE for streaming chat.
2. FastAPI validates the JWT and enforces ownership before every user-owned operation. Supabase PostgreSQL holds application rows; private object storage holds original files.
3. A Celery worker parses, cleans, chunks, embeds, and indexes document content. Qdrant holds active searchable chunks and metadata. Redis is ephemeral cache, rate-limit, and task-broker infrastructure.
4. Chat uses LangGraph to retrieve within one user and knowledge base, rerank, gate evidence, generate a grounded answer, validate citations against trusted metadata, and persist the conversation.
5. Kafka carries document, chat, usage, and audit events after those actions occur. It is outside the synchronous chat response path.

## Persistence and security boundaries

Supabase Auth owns identities. PostgreSQL owns knowledge bases, documents, conversations, messages, feedback, usage records, and audit logs. Qdrant stores searchable chunks, not originals. Redis must not become durable business storage. Every Qdrant search must filter by authenticated `user_id`, selected `knowledge_base_id`, and active status. RLS complements, but does not replace, FastAPI ownership checks.

## Implementation sequence

Module 0 creates the repository conventions and runnable entry points. Module 1 adds Supabase Auth and the PostgreSQL connection. Module 2 adds relational models and migrations. Module 3 adds the core Docker infrastructure. Modules 4–7 build and evaluate the first retrieval and answer path. Modules 8–13 add ownership, asynchronous lifecycle, production orchestration, and conversations. Modules 14–16 build the user portal. Modules 17–24 add events, analytics, observability, hardening, delivery, load tests, and portfolio material.

## Decisions to resolve in their scheduled modules

- Supabase project URL, anon key, hosted database connection, and JWT verification details require a real project before Module 1 can pass acceptance.
- The docs list tables and fields but do not define every enum, unique constraint, index, or RLS policy. Resolve these in Module 2 with ownership tests.
- Storage provider selection is MinIO locally or Supabase Storage; Module 4 chooses the first implementation behind the required interface.
- BGE-M3 index shape, embedding dimension, and model deployment need to be fixed before Qdrant collection creation in Module 4/5.
- Upload size limits, file sniffing rules, and parser fallback behavior need concrete values in Module 5.
- Retrieval thresholds and chunk sizes remain hypotheses until Module 7 evaluation; the docs explicitly require measurement.
- Event reliability and duplicate handling need design in Module 17; Kafka must not delay the chat response.

## Module 0 acceptance

- Git repository exists; scaffold directories match the project layout.
- FastAPI exposes `GET /health`.
- Next.js App Router page runs using JavaScript and Tailwind.
- shadcn/ui is initialized through its CLI and `components.json` is present.
- `.env.example`, `.gitignore`, README, Makefile, Dockerfiles, and lint/test commands are present.
- Unit, integration, API, RAG, and future E2E/evaluation locations are present.

## Verification and supplied UI preset

The supplied shadcn preset `b3QwSmN2e` was applied to the existing JavaScript Next.js app using `init --force --reinstall`. It uses the Base Nova style with a zinc base color. The CLI reported that six already installed UI component files matched its output and left those files intact; it updated the theme configuration and CSS. Product screen design is deferred until the separate template code is supplied.

Module 0 checks: backend Ruff lint and format checks pass; Pytest passes; frontend ESLint and Prettier checks pass; the Next.js production build succeeds. The API `/health` route and frontend root page returned successful HTTP responses in local runtime checks.

Some Module 1 authentication files were already started before the Module 0-only request. They compile and their isolated backend tests pass, but Module 1 is incomplete because no Supabase project is configured or live registration/login verified. They should not be treated as completed Module 1 work.
