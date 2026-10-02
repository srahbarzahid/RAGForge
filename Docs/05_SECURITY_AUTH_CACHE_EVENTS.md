# RAGForge — Security, Supabase Auth, Redis, Celery and Kafka

## Supabase Auth
Use Supabase Auth for registration, login, logout, refresh/session handling, and password reset later.

FastAPI validates Bearer JWT and derives authenticated user ID. Do not build a parallel password/JWT system.

## Authorization
Every knowledge base, document, conversation, and feedback operation verifies ownership by the authenticated user.

## RLS
Where direct Supabase table access exists, use RLS such as `user_id = auth.uid()`. Backend authorization remains mandatory.

## File Security
Validate extension, MIME, size, checksum, corruption, and sanitized filename. Keep storage private. Add malware scanning later if needed.

## Prompt Injection
User input and document content are untrusted. Retrieved text cannot override system instructions or request secrets/tools. Authorization always occurs before retrieval.

## Rate Limiting
Redis-based per-user limits for chat, uploads, and expensive reindex operations. Return 429 when exceeded.

## Redis
Use for rate limits, Celery broker/backend, cache, temporary helper state. Never as durable business DB.

## Celery — “DO THIS”
Tasks:
- PROCESS_DOCUMENT
- REINDEX_DOCUMENT
- DELETE_DOCUMENT_DATA
- REBUILD_KNOWLEDGE_BASE
- CLEANUP_EXPIRED_DATA

Use bounded retries and idempotency where practical.

## Kafka — “THIS HAPPENED”
Topics:
- `rag.document.events`
- `rag.chat.events`
- `rag.usage.events`
- `rag.audit.events`

Events:
- DOCUMENT_READY
- DOCUMENT_FAILED
- DOCUMENT_DELETED
- KNOWLEDGE_BASE_UPDATED
- CHAT_COMPLETED
- CHAT_FAILED
- CHAT_ABSTAINED
- USAGE_RECORDED

Event envelope includes event_id, event_type, event_version, occurred_at, user_id, resource_id, payload.

Kafka is never used to deliver the synchronous chat response.

## Secrets
Browser may use only Supabase public/anon client configuration required by Supabase. Never expose service-role key, DB password, LLM keys, Qdrant admin secrets, Kafka credentials, or storage secrets.

## CORS
Allow only expected frontend origins in production.
