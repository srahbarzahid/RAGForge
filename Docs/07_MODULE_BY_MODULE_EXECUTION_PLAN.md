# RAGForge — Authoritative Module-by-Module Execution Plan

> This is the primary implementation document for coding agents.

> Current project context: RAGForge is being built for learning, skill development, experimentation, and portfolio/CV strength. There is no assumed current client count. Build production-style foundations without inventing commercial requirements.

## Critical Rule
Do not redesign architecture, data flow, persistence boundaries, or orchestration. Do not reintroduce the removed external bot/widget/API-key product.

---

# MODULE 0 — Repository Bootstrap

## Goal
Create exact monorepo structure and development conventions.

## Tasks
- initialize Git;
- create scaffold from `02_PROJECT_SCAFFOLD.md`;
- add `.env.example`, `.gitignore`, README, Makefile;
- initialize FastAPI backend;
- initialize Next.js frontend using JavaScript;
- configure Tailwind and shadcn/ui;
- add lint/format/test commands;
- create unit/integration/E2E/RAG test folders.

## Done When
- FastAPI health endpoint works;
- Next.js page runs;
- lint/test commands work;
- scaffold matches docs.

---

# MODULE 1 — Supabase Auth and Database Foundation

## Goal
Establish identity and relational persistence first.

## Tasks
- create Supabase project;
- enable email/password Auth;
- configure frontend Supabase client;
- configure backend connection to Supabase PostgreSQL;
- configure backend JWT verification;
- add frontend register/login/logout/session refresh;
- create initial RLS approach;
- document env vars.

## Done When
- user registers/logs in;
- frontend receives valid session;
- FastAPI `/auth/me` validates Supabase JWT.

---

# MODULE 2 — Relational Schema and Migrations

## Implement
- profiles;
- knowledge_bases;
- documents;
- conversations;
- messages;
- feedback;
- usage_records;
- audit_logs.

## Tasks
- SQLAlchemy models;
- Alembic migrations;
- indexes/FKs;
- user ownership fields;
- RLS policies where direct Supabase access is possible.

## Done When
- schema can be recreated cleanly;
- ownership constraints are tested.

---

# MODULE 3 — Docker and Core Infrastructure

## Docker Compose
- api;
- frontend;
- redis;
- qdrant;
- minio;
- kafka;
- worker;
- optional Ollama.

Supabase stays hosted unless local Supabase is intentionally added later.

## Done When
- API reaches Redis/Qdrant/MinIO/Kafka;
- frontend reaches FastAPI;
- health checks pass.

---

# MODULE 4 — Storage, Redis and Qdrant Adapters

## Storage
Create `StorageProvider` and implement MinIO or Supabase Storage provider.

## Redis
Create reusable connection/cache/rate-limit primitives.

## Qdrant
Create collection setup, upsert, filtered search, document deletion, KB deletion.

## Critical
All vector search must support filters for `user_id` and `knowledge_base_id`.

## Done When
Integration tests verify file round-trip, cache operations, vector search and ownership filtering.

---

# MODULE 5 — Basic Document Ingestion

## Goal
Make PDF/DOCX/TXT searchable.

## Tasks
- upload validation;
- storage save;
- Docling parser;
- PyMuPDF fallback;
- text cleanup;
- structure detection;
- heading/paragraph/sentence-aware chunking;
- 500/800/75 initial token config;
- metadata enrichment;
- BGE-M3 embeddings;
- Qdrant indexing.

Initially this may run synchronously for development.

## Done When
A sample document is indexed and its chunks can be retrieved.

---

# MODULE 6 — Basic RAG Vertical Slice

## Implement
- query embeddings;
- Qdrant dense retrieval;
- BGE reranking;
- context builder;
- LLMProvider abstraction;
- Gemini or Ollama provider;
- trusted answer citations.

## Done When
A known document can answer multiple questions with correct source/page evidence.

---

# MODULE 7 — RAG Evaluation and Chunk Calibration

## Tasks
- create representative QA dataset;
- record expected document/page;
- compare 300/500/750 and structure-aware chunking;
- measure Recall@K and MRR;
- evaluate faithfulness, answer relevance, citation correctness and abstention.

## Done When
Default RAG configuration is based on measured results rather than guessing.

---

# MODULE 8 — User-Owned Knowledge Bases

## Implement
- KB CRUD;
- authenticated ownership;
- document ownership;
- conversation ownership;
- user-scoped Qdrant payload filters.

## Critical Test
User A must never retrieve User B content.

---

# MODULE 9 — Celery Async Document Processing

## Goal
Remove long document work from HTTP requests.

## Implement
- Redis broker/backend;
- Celery app;
- `process_document` task;
- status transitions;
- retries/backoff;
- processing error persistence;
- idempotency safeguards.

Upload endpoint returns `202 Accepted` with document ID and status.

---

# MODULE 10 — Document Lifecycle

## Implement
- checksum duplicate detection;
- delete workflow;
- Qdrant cleanup;
- object cleanup;
- reindex;
- versioning;
- safe vector replacement;
- cache invalidation.

## Done When
Old active content cannot remain searchable after successful replacement/deletion.

---

# MODULE 11 — LangGraph Production Orchestration

## Nodes
- validate_request;
- load_conversation_context;
- normalize_query;
- classify_query;
- rewrite_query;
- retrieve_dense;
- retrieve_lexical;
- fuse_results;
- rerank;
- deduplicate;
- evaluate_evidence;
- build_context / abstain;
- generate_answer;
- validate_grounding;
- build_citations;
- persist_message;
- publish_event.

## Done When
All production chat requests use the graph and nodes can be tested independently.

---

# MODULE 12 — Hybrid Retrieval and Evidence Gate

## Implement
- BM25 or equivalent lexical search;
- reciprocal rank fusion;
- candidate Top-K;
- BGE reranking;
- near-duplicate suppression;
- evidence threshold;
- controlled abstention.

Re-run RAG evaluation and document changes.

---

# MODULE 13 — Conversations and SSE Streaming

## Implement
- conversation creation;
- message persistence;
- recent history;
- contextual query rewrite;
- SSE token streaming;
- disconnect/error handling;
- feedback endpoint;
- usage metadata.

---

# MODULE 14 — Next.js Portal Foundation

## Implement
- register/login pages using Supabase Auth;
- protected routes;
- dashboard shell;
- shadcn sidebar/layout;
- TanStack Query provider;
- REST service layer;
- React Hook Form + Zod patterns.

---

# MODULE 15 — Knowledge Base and Document UI

## Implement
- KB list/create/detail;
- document upload;
- processing status;
- READY/FAILED states;
- delete;
- reindex;
- error display.

Use shadcn components rather than custom copies.

---

# MODULE 16 — Chat and Conversation UI

## Implement
- KB-specific chat;
- create/resume conversation;
- SSE streaming;
- citations/source display;
- retry/error states;
- feedback;
- conversation list/history.

---

# MODULE 17 — Kafka Event Plane

## Topics
- `rag.document.events`
- `rag.chat.events`
- `rag.usage.events`
- `rag.audit.events`

## Producers
Publish document lifecycle, chat completion/abstention, usage and audit events.

## Consumers
- analytics;
- usage;
- audit.

## Critical
Do not route the user chat response through Kafka.

---

# MODULE 18 — Analytics

## Metrics
- total questions;
- conversation count;
- document counts/statuses;
- average/P95 latency;
- no-answer rate;
- feedback;
- token usage;
- estimated model cost;
- processing failure count.

---

# MODULE 19 — Observability

## Implement
- structured JSON logs;
- request IDs;
- Langfuse RAG traces;
- Prometheus metrics;
- Grafana dashboards.

## Done When
A developer can investigate a specific bad answer from request through retrieval/reranking/model output.

---

# MODULE 20 — Security Hardening

Verify:
- Supabase JWT validation;
- RLS where applicable;
- backend ownership checks;
- strict CORS;
- rate limiting;
- private storage;
- safe secrets;
- file validation;
- prompt-injection protections;
- privacy-aware logging;
- user-isolation regression suite.

---

# MODULE 21 — CI/CD

## GitHub Actions
PR: lint, unit, integration, selected RAG regression, security scan, build verification.

Main/tag: Docker build, registry push, staging deploy, migrations, smoke tests, controlled production promotion.

---

# MODULE 22 — Kubernetes

Only after Docker Compose works end-to-end.

Implement Deployments, Services, Ingress, ConfigMaps, Secrets, readiness/liveness probes, resource requests/limits, HPA, rolling updates and rollback.

Supabase remains external managed Auth/PostgreSQL.

---

# MODULE 23 — Load and Reliability

Use k6 for staged 10/50/100/250/500 concurrent chat-request scenarios. Measure P50/P95/P99, throughput, errors, DB connections, Qdrant latency and LLM latency.

Test worker crash, API restart, duplicate task/event, Qdrant/storage/LLM timeout, malformed document and reindex failure.

---

# MODULE 24 — Portfolio Packaging

Deliver architecture diagrams, README, API docs, screenshots, RAG evaluation report, deployment guide, ADRs, measured benchmarks, CV description and interview talking points.

Never claim unmeasured performance.
