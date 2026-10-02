# RAGForge — Final Stack and Decisions

## Frontend
Next.js, React, JavaScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Recharts, Lucide.

## Backend
Python, FastAPI, Pydantic, SQLAlchemy, Alembic.

## Authentication
Supabase Auth, Supabase JWT, FastAPI verification.

## Main Database
Supabase PostgreSQL.

## Vector DB
Qdrant.

## Document Storage
Supabase Storage or MinIO locally through a StorageProvider abstraction; S3-compatible later.

## Cache
Redis.

## Background Jobs
Celery.

## Event Streaming
Apache Kafka.

## RAG
LangGraph, Docling, PyMuPDF, BGE-M3, BGE Reranker, hybrid retrieval, evidence gate, trusted citations.

## LLM
Gemini, OpenAI, Ollama through LLMProvider.

## Communication
REST API; SSE for chat streaming.

## DevOps
Docker, Docker Compose, Kubernetes, Nginx/Ingress, GitHub Actions.

## Observability
Langfuse, Prometheus, Grafana, structured logs.

## Testing
Pytest, HTTPX, Playwright, k6, RAGAS.

## Removed
Public bot creation, website chatbot widget, embed script, third-party bot API, client API-key product, domain allow-list bot logic.
