# RAGForge — Project Scaffold

```text
ragforge/
├── frontend/
│   ├── app/
│   │   ├── (auth)/login/
│   │   ├── (auth)/register/
│   │   ├── (dashboard)/dashboard/
│   │   ├── (dashboard)/knowledge-bases/
│   │   ├── (dashboard)/knowledge-bases/[knowledgeBaseId]/
│   │   ├── (dashboard)/documents/
│   │   ├── (dashboard)/chat/[knowledgeBaseId]/
│   │   ├── (dashboard)/conversations/[conversationId]/
│   │   ├── (dashboard)/analytics/
│   │   └── (dashboard)/settings/
│   ├── components/{ui,layout,knowledge,documents,chat,analytics,shared}/
│   ├── hooks/
│   ├── lib/supabase/
│   ├── services/{knowledgeBases,documents,chat,conversations,analytics}.js
│   ├── schemas/
│   ├── components.json
│   ├── package.json
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/v1/{auth,knowledge_bases,documents,chat,conversations,feedback,analytics}.py
│   │   ├── core/{config,security,logging,exceptions,dependencies}.py
│   │   ├── modules/{users,knowledge_bases,documents,conversations,chat,feedback,analytics,usage,audit}/
│   │   ├── rag/
│   │   │   ├── graph/
│   │   │   ├── ingestion/
│   │   │   ├── chunking/
│   │   │   ├── embeddings/
│   │   │   ├── retrieval/
│   │   │   ├── reranking/
│   │   │   ├── prompts/
│   │   │   ├── citations/
│   │   │   ├── evaluation/
│   │   │   └── providers/
│   │   ├── infrastructure/{database,supabase,qdrant,storage,redis,celery,kafka}/
│   │   └── schemas/
│   ├── migrations/
│   ├── tests/{unit,integration,api,rag}/
│   ├── requirements.txt
│   └── Dockerfile
│
├── workers/
│   ├── ingestion/
│   └── consumers/{analytics_consumer,usage_consumer,audit_consumer}.py
├── evaluation/{datasets,retrieval,generation,reports}/
├── infrastructure/{docker,kubernetes,nginx,monitoring,terraform}/
├── docs/{architecture,diagrams,api,adr,implementation}/
├── scripts/{dev,db,seed,evaluation}/
├── .github/workflows/
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

## Backend Module Pattern
```text
module/
├── model.py
├── schema.py
├── repository.py
├── service.py
├── permissions.py
└── exceptions.py
```

## Required Abstractions
### StorageProvider
`upload`, `download`, `delete`, `exists`, `signed_url`

### LLMProvider
`generate`, `stream`

### EmbeddingProvider
`embed_documents`, `embed_query`

### VectorRepository
`upsert_chunks`, `search`, `delete_document`, `delete_knowledge_base`

Business modules should not directly depend on vendor SDKs where an adapter is appropriate.
