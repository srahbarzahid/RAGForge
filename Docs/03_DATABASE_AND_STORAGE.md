# RAGForge — Supabase Database, Storage, Qdrant and Redis

## Responsibility Map
| Data | System |
|---|---|
| Identities | Supabase Auth |
| Relational app data | Supabase PostgreSQL |
| Original files | Supabase Storage / MinIO / S3 |
| Embeddings/chunks | Qdrant |
| Cache/rate limits/Celery | Redis |
| Events | Kafka |

## Tables
Supabase Auth owns `auth.users`.

### profiles
- id UUID PK/FK auth.users
- full_name
- status
- created_at
- updated_at

### knowledge_bases
- id UUID PK
- user_id UUID NOT NULL
- name
- description
- status
- embedding_provider
- embedding_model
- chunk_strategy
- chunk_target_tokens
- chunk_max_tokens
- chunk_overlap_tokens
- version
- created_at
- updated_at

### documents
- id UUID PK
- user_id UUID NOT NULL
- knowledge_base_id UUID FK
- filename
- original_filename
- mime_type
- size_bytes
- storage_key
- checksum
- status
- version
- is_active
- page_count
- chunk_count
- processing_error
- created_at
- updated_at
- deleted_at

### conversations
- id UUID PK
- user_id UUID NOT NULL
- knowledge_base_id UUID FK
- title
- status
- started_at
- last_activity_at

### messages
- id UUID PK
- conversation_id UUID FK
- role
- content
- model
- input_tokens
- output_tokens
- latency_ms
- created_at

### feedback
- id UUID PK
- user_id UUID
- message_id UUID FK
- rating
- comment
- created_at

### usage_records
- id UUID PK
- user_id UUID
- knowledge_base_id UUID NULL
- request_type
- input_tokens
- output_tokens
- embedding_tokens
- latency_ms
- estimated_cost
- created_at

### audit_logs
- id UUID PK
- user_id UUID
- action
- resource_type
- resource_id
- metadata JSONB
- ip_address
- created_at

## RLS
Enable RLS where direct Supabase access is possible. Base rule for user-owned rows: `user_id = auth.uid()`. FastAPI must still enforce ownership independently.

## Qdrant Payload
```text
user_id
knowledge_base_id
document_id
document_name
document_version
chunk_index
content
page_start
page_end
section
subsection
parent_chunk_id
token_count
is_active
```

Every search filters authenticated `user_id`, selected `knowledge_base_id`, and `is_active=true`.

## Document Storage
Use a private bucket/path:
```text
users/<user_id>/knowledge-bases/<kb_id>/documents/<document_id>/versions/<n>/original.ext
```

Local development may use MinIO. Hosted simplified deployment may use Supabase Storage. Keep a StorageProvider abstraction so S3 can be added later.

## Redis
Use for cache, rate limits, Celery broker/backend, locks, temporary state. Not durable business data.

Suggested keys:
```text
kb:<id>:version
rate:chat:user:<id>
rate:upload:user:<id>
```

## Delete Flow
`request → auth/ownership → mark DELETING → Celery → remove Qdrant → remove object → invalidate cache → mark DELETED → Kafka event`

## Versioning
Process new version first, validate, activate new vectors, then deactivate old vectors and increment KB version. Never expose old and new conflicting policies together as active evidence.
