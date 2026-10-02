# RAGForge — REST API and Frontend Workflows

## Communication
```text
Next.js → REST → FastAPI
Chat → REST request + SSE stream
Next.js ↔ Supabase Auth for authentication/session
```

API prefix: `/api/v1`.

## Auth
- `GET /auth/me`
- optional `POST /auth/sync-profile`

Registration/login/logout are primarily Supabase Auth SDK operations.

## Knowledge Bases
- `POST /knowledge-bases`
- `GET /knowledge-bases`
- `GET /knowledge-bases/{id}`
- `PATCH /knowledge-bases/{id}`
- `DELETE /knowledge-bases/{id}`

## Documents
- `POST /knowledge-bases/{kbId}/documents`
- `GET /knowledge-bases/{kbId}/documents`
- `GET /documents/{documentId}`
- `DELETE /documents/{documentId}`
- `POST /documents/{documentId}/reindex`

Upload returns 202 with document ID/status.

## Chat
- `POST /knowledge-bases/{kbId}/chat`

Body: message + optional conversation_id. Stream response with SSE.

## Conversations
- `GET /conversations`
- `GET /conversations/{id}`
- `GET /conversations/{id}/messages`
- `DELETE /conversations/{id}`

## Feedback
- `POST /messages/{messageId}/feedback`

## Analytics
- `GET /analytics/overview`
- `GET /analytics/usage`
- `GET /analytics/documents`
- `GET /analytics/feedback`

## Frontend Pages
`/register, /login, /dashboard, /knowledge-bases, /knowledge-bases/new, /knowledge-bases/[id], /documents, /chat/[knowledgeBaseId], /conversations, /conversations/[id], /analytics, /settings`.

## shadcn/ui
Use Sidebar, Card, Table, Badge, Button, Input, Textarea, Dialog, Sheet, Tabs, Select, Alert, Progress, Skeleton, Tooltip, DropdownMenu, Sonner, Breadcrumb, Pagination before custom equivalents.

## Frontend Data Flow
`Component → TanStack Query → service function → FastAPI REST → response → TanStack cache → UI`.

## Upload UI
`select file → client validation → upload → QUEUED → poll/refresh status → PARSING → CHUNKING → EMBEDDING → INDEXING → READY`.

## Chat UI
Select KB, start/resume conversation, ask question, stream response, show citations, show errors/retry, allow feedback.
