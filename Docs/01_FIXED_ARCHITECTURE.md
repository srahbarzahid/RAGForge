# RAGForge — Fixed Architecture

> Authoritative architecture. Do not redesign without explicit project-owner approval.

## Product Boundary
RAGForge is a logged-in document intelligence/RAG portal.

```text
Register/Login → Create KB → Upload → Process → Chat → Answer + Citation
```

Removed from scope: public bots, embed scripts, external chatbot APIs, client API keys, anonymous public chat, allowed-domain widget logic.

## Runtime Architecture
```text
USER
 ↓
Next.js + React + shadcn/ui
 ↓
Supabase Auth
 ↓ JWT
FastAPI REST API
 ├── Knowledge/Data → Supabase PostgreSQL
 ├── Document Upload → Object Storage → Celery Worker
 ├── Cache/Rate Limit → Redis
 └── Chat/RAG → LangGraph → Qdrant → LLM

Celery Worker:
Storage → Parse → Clean → Chunk → Embed → Qdrant → READY

Event Plane:
FastAPI/Worker → Kafka → Analytics / Usage / Audit

Observability:
Langfuse + Prometheus + Grafana
```

## Frontend
- Next.js App Router
- React
- JavaScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- React Hook Form
- Zod
- Recharts

Frontend responsibilities: auth UI, dashboard, KB/document management, chat, conversations, analytics, settings.

Frontend must never hold service-role keys, DB passwords, Qdrant admin secrets, Kafka secrets, or LLM provider secrets.

## Authentication
Supabase Auth is authoritative.

```text
Next.js → Supabase Auth → JWT → FastAPI → validate JWT → user context
```

## Backend
FastAPI owns application/business logic: authorization, KB/document CRUD, upload orchestration, conversations, RAG, analytics APIs, event publishing.

## Data Boundaries
- Supabase Auth: user identities.
- Supabase PostgreSQL: application relational data.
- Qdrant: active searchable vector chunks.
- Supabase Storage/MinIO/S3: original documents.
- Redis: cache, rate limiting, Celery broker/backend, temporary state.
- Kafka: domain events.

## Document Pipeline
```text
Upload → JWT → ownership → validate → storage → DB row → Celery → parse → clean → chunk → embed → Qdrant → READY → Kafka
```

## RAG Pipeline
```text
Question → JWT → KB ownership → history → LangGraph → rewrite → dense+lexical → fusion → rerank → evidence gate → context → LLM → citation validation → persist → SSE
```

## Chunking Defaults
- target 500 tokens
- max 800 tokens
- overlap 75 tokens
- preserve headings/lists/tables/FAQ pairs

Tune only through evaluation.

## Communication
- Next.js ↔ FastAPI: REST.
- Chat output: SSE.
- Next.js ↔ Supabase: authentication/session only, plus deliberately chosen RLS-protected direct reads if ever needed.

## Deployment
Local: Docker Compose.
Production-style: Kubernetes for frontend/API/workers/consumers; Supabase remains managed/external.

## Forbidden Changes
Do not replace Next.js, FastAPI, Supabase Auth, Supabase PostgreSQL, Qdrant, REST/SSE, Redis, Celery, Kafka, or LangGraph without approval. Do not reintroduce widget/bot-as-a-service architecture.
