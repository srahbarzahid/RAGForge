# RAGForge — Master Project Plan

## Purpose
RAGForge is a secure RAG document intelligence portal built for learning, engineering skill development, experimentation, and portfolio/CV strength.

Authenticated users can register, log in, create private knowledge bases, upload PDF/DOCX/TXT documents, wait for automatic processing, and then ask questions against a selected knowledge base. Answers must be grounded in indexed documents and include trusted citations.

Current scope explicitly excludes public chatbot widgets, third-party bot embedding, external client API keys, and bot-as-a-service features.

## Final User Journey
```text
Register / Login
  ↓
Supabase Auth
  ↓
Next.js Portal
  ↓
Create Knowledge Base
  ↓
Upload Documents
  ↓
FastAPI REST API
  ↓
Object Storage
  ↓
Celery Processing
  ↓
Parse → Clean → Chunk → Embed
  ↓
Qdrant
  ↓
Document READY
  ↓
Open Chat
  ↓
Ask Question
  ↓
LangGraph RAG
  ↓
Hybrid Retrieval → Reranker → Evidence Gate
  ↓
LLM
  ↓
Answer + Citations
  ↓
Conversation Stored
```

## Final Stack
- Frontend: Next.js, React, JavaScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Recharts, Lucide.
- Backend: Python, FastAPI, Pydantic, SQLAlchemy, Alembic.
- Auth + relational DB: Supabase Auth + Supabase PostgreSQL.
- Vector DB: Qdrant.
- Document storage: Supabase Storage or MinIO locally behind a StorageProvider abstraction.
- Cache/broker: Redis.
- Background jobs: Celery.
- Events: Apache Kafka.
- Parsing: Docling + PyMuPDF fallback.
- Embeddings: BGE-M3.
- Reranker: BGE Reranker.
- RAG orchestration: LangGraph.
- LLM providers: Gemini, OpenAI, Ollama through a provider abstraction.
- Communication: REST API; SSE for streaming chat.
- DevOps: Docker, Docker Compose, Kubernetes, Nginx/Ingress, GitHub Actions.
- Observability: Langfuse, Prometheus, Grafana, structured JSON logging.
- Testing: Pytest, HTTPX, Playwright, k6, RAGAS.

## Fixed Architectural Decisions
1. Supabase Auth is the identity provider; do not build a parallel custom password/JWT system.
2. Supabase PostgreSQL is the main relational database.
3. FastAPI is the main business/RAG backend.
4. Next.js communicates with FastAPI using REST; chat streams using SSE.
5. Frontend may use Supabase directly for authentication/session handling.
6. Private application workflows remain behind FastAPI.
7. Qdrant stores embeddings/chunk payload, never raw source files.
8. Raw documents live in private object storage.
9. Redis is ephemeral infrastructure only.
10. Celery means “do this job”; Kafka means “this event happened”.
11. Kafka is not part of the synchronous chat path.
12. All retrieval must verify authenticated user ownership and selected knowledge base.
13. The system must abstain when evidence is insufficient.
14. No external website bot/widget feature in current scope.

## Core Domain
```text
User
 ├── Knowledge Bases
 │    └── Documents
 │         └── Chunks / Vectors
 ├── Conversations
 │    └── Messages
 ├── Feedback
 ├── Usage Records
 └── Audit Logs
```

## Build Order
```text
Repository/Scaffold
 ↓
Supabase Auth + PostgreSQL
 ↓
Docker + Redis + Qdrant + Storage + Kafka
 ↓
Database Schema
 ↓
Storage/Qdrant/Redis Adapters
 ↓
Document Ingestion
 ↓
Basic RAG Vertical Slice
 ↓
RAG Evaluation
 ↓
User-Owned Knowledge Bases
 ↓
Celery Async Processing
 ↓
Document Lifecycle
 ↓
LangGraph
 ↓
Hybrid Retrieval + Reranking
 ↓
Conversations + SSE
 ↓
Next.js Portal
 ↓
Kafka Analytics/Usage/Audit
 ↓
Observability
 ↓
CI/CD
 ↓
Kubernetes
```

See `07_MODULE_BY_MODULE_EXECUTION_PLAN.md` for the authoritative execution sequence.
