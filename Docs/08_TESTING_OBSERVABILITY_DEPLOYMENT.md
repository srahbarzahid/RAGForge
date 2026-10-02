# RAGForge — Testing, Observability and Deployment

## Unit
Chunking, permissions, JWT validation adapter, citation mapping, query normalization, fusion, evidence gate, provider adapters.

## Integration
Supabase/Postgres test schema, Redis, Qdrant, MinIO/Supabase Storage, Kafka, Celery. Critical ownership and vector-filter tests are mandatory.

## API
Test invalid/valid token, unauthorized KB, upload, status, delete, reindex, chat, SSE, conversations, analytics.

## RAG Regression
Dataset contains question, expected answer, expected document, expected page. Measure Recall@K, MRR, faithfulness, relevance, citation correctness, abstention.

## E2E
Playwright: register/login → create KB → upload → wait READY → chat → verify answer/citation → verify conversation.

## Observability
Structured logs: request_id, user_id, KB ID, endpoint, status, latency, error code.

Langfuse: original/rewrite query, chunk IDs, retrieval/reranker scores, context IDs, model, token usage, latency, response metadata.

Prometheus: HTTP latency/errors, RAG retrieval/reranker latency, abstentions, LLM latency/errors/tokens, document processing success/failure, Celery queue depth, Kafka lag, Qdrant latency.

Grafana: platform health, RAG latency, LLM health, document pipeline, Kafka/Celery, usage.

## CI
Lint → unit → integration → RAG regression subset → security scan → build verification.

## CD
Docker build → registry → staging → migrations → smoke tests → controlled production rollout.

## Kubernetes
Deploy frontend, API, workers, and Kafka consumers with Deployments, Services, Ingress, ConfigMaps, Secrets, readiness/liveness probes, resource limits, HPA, rolling updates. Supabase remains external managed auth/database.

## Reliability Scenarios
API restart, worker crash, duplicate Celery task, Kafka duplicate, Qdrant/storage timeout, LLM timeout, malformed PDF, reindex failure.
