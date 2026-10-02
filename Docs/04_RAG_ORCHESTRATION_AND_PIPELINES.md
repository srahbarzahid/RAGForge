# RAGForge — RAG Orchestration and Pipelines

## Ingestion Pipeline
```text
Authenticated User
 ↓
Upload PDF/DOCX/TXT
 ↓
FastAPI REST
 ↓
JWT validation
 ↓
KB ownership check
 ↓
file type/size/checksum validation
 ↓
Object Storage
 ↓
Supabase PostgreSQL document row
 ↓
Celery
 ↓
Worker
 ↓
Docling / PyMuPDF
 ↓
Clean + Structure Detection
 ↓
Chunk
 ↓
Metadata Enrichment
 ↓
BGE-M3
 ↓
Qdrant
 ↓
READY
 ↓
Kafka DOCUMENT_READY
```

Document states: `UPLOADED, QUEUED, PARSING, CHUNKING, EMBEDDING, INDEXING, READY, FAILED, DELETING, DELETED`.

## Chunking
Defaults: target 500, max 800, overlap 75 tokens.

Rules: preserve headings, paragraphs, lists, table headers, and FAQ Q+A pairs. Avoid sentence splitting unless required.

## Query Pipeline
```text
Question
 ↓
FastAPI
 ↓
JWT + KB ownership
 ↓
Recent conversation
 ↓
LangGraph
 ↓
Normalize / Rewrite
 ↓
Dense Retrieval + Lexical Retrieval
 ↓
RRF Fusion
 ↓
BGE Reranker
 ↓
Deduplicate
 ↓
Evidence Gate
 ├─ insufficient → abstain
 └─ sufficient → Context Builder
                    ↓
                 LLM Provider
                    ↓
              Grounded Answer
                    ↓
            Citation Validation
                    ↓
              Persist Message
                    ↓
           Kafka CHAT_COMPLETED
                    ↓
                 SSE Stream
```

## LangGraph State
`request_id, user_id, knowledge_base_id, conversation_id, original_query, normalized_query, rewritten_query, recent_messages, dense_results, lexical_results, fused_results, reranked_results, evidence_status, context_blocks, answer, citations, model_metadata, usage, errors`.

## Nodes
`validate_request → load_context → normalize → classify → rewrite_if_needed → retrieve_dense → retrieve_lexical → fuse → rerank → deduplicate → evaluate_evidence → build_context/abstain → generate → validate_grounding → build_citations → persist → publish_event`.

## Evidence Gate
If evidence is insufficient, answer: “I couldn't find sufficient information in the selected knowledge base to answer that question.” Thresholds must be calibrated from evaluation data.

## Trusted Citations
LLM references internal source IDs. Backend maps them to trusted document/page/section metadata. Never trust arbitrary model-created citation metadata.

## Conversation Memory
Store all messages in PostgreSQL. Send only recent turns plus optional summary later. Conversation memory helps rewrite queries; it never replaces retrieval.

## Provider Abstraction
`GeminiProvider`, `OpenAIProvider`, `OllamaProvider` implement common `generate()` and `stream()`.

## Evaluation
Retrieval: Recall@K, Precision@K, MRR.
Generation: faithfulness, relevance, citation correctness, abstention correctness.
Compare 300/500/750-token and structure-aware chunking strategies.
