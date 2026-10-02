# RAGForge — Coding Agent Rules

## Mandatory Read Order
Read all numbered project docs before implementation; `07_MODULE_BY_MODULE_EXECUTION_PLAN.md` controls sequencing.

## Architecture Freeze
Do not replace Next.js/React/JavaScript, shadcn/Tailwind, FastAPI, REST/SSE, Supabase Auth/PostgreSQL, Qdrant, Redis, Celery, Kafka, LangGraph, Docker/Kubernetes without approval.

Do not reintroduce public bots, widgets, embed scripts, third-party chatbot APIs, or client API-key product features.

## Authentication
No parallel custom login/password/JWT system. FastAPI validates Supabase JWT.

## Data Ownership
Every user-owned resource query must verify authenticated user ownership. Every Qdrant search filters user_id + knowledge_base_id.

## Module Discipline
Implement only the current module, required prerequisites, and related tests. Do not add future infrastructure early.

## RAG Safety
Never skip auth before retrieval, treat document text as system instructions, answer when evidence gate fails, invent citations, or mix incompatible embeddings in one active index.

## Frontend
Prefer shadcn/ui. Use TanStack Query for server state and React Hook Form + Zod for forms. Do not add Redux without a real requirement.

## Secrets
Never commit/log service-role keys, DB passwords, JWTs, LLM keys, storage credentials, Qdrant secrets, or Kafka credentials.

## Definition of Done
Implementation works, tests and lint pass, migrations/config documented, no architecture deviation, module acceptance criteria satisfied.
