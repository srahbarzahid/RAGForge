"""Create user-owned application tables with closed Data API access.

Revision ID: 20261002_01
Revises:
"""

# ruff: noqa: E501

from alembic import op

revision = "20261002_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = """
        CREATE TABLE public.profiles (
            id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
            full_name text,
            status text NOT NULL DEFAULT 'ACTIVE',
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now()
        );

        CREATE TABLE public.knowledge_bases (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid NOT NULL REFERENCES auth.users(id),
            name text NOT NULL CHECK (length(btrim(name)) > 0),
            description text,
            status text NOT NULL DEFAULT 'ACTIVE',
            embedding_provider text,
            embedding_model text,
            chunk_strategy text,
            chunk_target_tokens integer NOT NULL DEFAULT 500 CHECK (chunk_target_tokens > 0),
            chunk_max_tokens integer NOT NULL DEFAULT 800 CHECK (chunk_max_tokens >= chunk_target_tokens),
            chunk_overlap_tokens integer NOT NULL DEFAULT 75 CHECK (chunk_overlap_tokens >= 0 AND chunk_overlap_tokens < chunk_target_tokens),
            version integer NOT NULL DEFAULT 1 CHECK (version > 0),
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now(),
            UNIQUE (id, user_id)
        );
        CREATE INDEX knowledge_bases_user_id_idx ON public.knowledge_bases(user_id);

        CREATE TABLE public.documents (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid NOT NULL REFERENCES auth.users(id),
            knowledge_base_id uuid NOT NULL,
            filename text NOT NULL,
            original_filename text NOT NULL,
            mime_type text NOT NULL,
            size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
            storage_key text NOT NULL UNIQUE,
            checksum text NOT NULL,
            status text NOT NULL DEFAULT 'UPLOADED' CHECK (status IN ('UPLOADED','QUEUED','PARSING','CHUNKING','EMBEDDING','INDEXING','READY','FAILED','DELETING','DELETED')),
            version integer NOT NULL DEFAULT 1 CHECK (version > 0),
            is_active boolean NOT NULL DEFAULT true,
            page_count integer CHECK (page_count >= 0),
            chunk_count integer CHECK (chunk_count >= 0),
            processing_error text,
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now(),
            deleted_at timestamptz,
            FOREIGN KEY (knowledge_base_id, user_id) REFERENCES public.knowledge_bases(id, user_id),
            UNIQUE (id, user_id)
        );
        CREATE INDEX documents_user_kb_idx ON public.documents(user_id, knowledge_base_id);
        CREATE INDEX documents_kb_status_idx ON public.documents(knowledge_base_id, status);

        CREATE TABLE public.conversations (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid NOT NULL REFERENCES auth.users(id),
            knowledge_base_id uuid NOT NULL,
            title text,
            status text NOT NULL DEFAULT 'ACTIVE',
            started_at timestamptz NOT NULL DEFAULT now(),
            last_activity_at timestamptz NOT NULL DEFAULT now(),
            FOREIGN KEY (knowledge_base_id, user_id) REFERENCES public.knowledge_bases(id, user_id),
            UNIQUE (id, user_id)
        );
        CREATE INDEX conversations_user_activity_idx ON public.conversations(user_id, last_activity_at DESC);
        CREATE INDEX conversations_kb_idx ON public.conversations(knowledge_base_id);

        CREATE TABLE public.messages (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid NOT NULL,
            conversation_id uuid NOT NULL,
            role text NOT NULL CHECK (role IN ('user','assistant','system','tool')),
            content text NOT NULL,
            model text,
            input_tokens integer CHECK (input_tokens >= 0),
            output_tokens integer CHECK (output_tokens >= 0),
            latency_ms integer CHECK (latency_ms >= 0),
            created_at timestamptz NOT NULL DEFAULT now(),
            FOREIGN KEY (conversation_id, user_id) REFERENCES public.conversations(id, user_id),
            UNIQUE (id, user_id)
        );
        CREATE INDEX messages_conversation_created_idx ON public.messages(conversation_id, created_at);
        CREATE INDEX messages_user_id_idx ON public.messages(user_id);

        CREATE TABLE public.feedback (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid NOT NULL,
            message_id uuid NOT NULL,
            rating integer NOT NULL CHECK (rating BETWEEN 1 AND 5),
            comment text,
            created_at timestamptz NOT NULL DEFAULT now(),
            FOREIGN KEY (message_id, user_id) REFERENCES public.messages(id, user_id),
            UNIQUE (user_id, message_id)
        );
        CREATE INDEX feedback_message_id_idx ON public.feedback(message_id);

        CREATE TABLE public.usage_records (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
            knowledge_base_id uuid REFERENCES public.knowledge_bases(id),
            request_type text NOT NULL,
            input_tokens integer NOT NULL DEFAULT 0 CHECK (input_tokens >= 0),
            output_tokens integer NOT NULL DEFAULT 0 CHECK (output_tokens >= 0),
            embedding_tokens integer NOT NULL DEFAULT 0 CHECK (embedding_tokens >= 0),
            latency_ms integer CHECK (latency_ms >= 0),
            estimated_cost numeric(18, 8) CHECK (estimated_cost >= 0),
            created_at timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX usage_records_user_created_idx ON public.usage_records(user_id, created_at DESC);
        CREATE INDEX usage_records_kb_idx ON public.usage_records(knowledge_base_id);

        CREATE TABLE public.audit_logs (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
            action text NOT NULL,
            resource_type text NOT NULL,
            resource_id uuid,
            metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
            ip_address inet,
            created_at timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX audit_logs_user_created_idx ON public.audit_logs(user_id, created_at DESC);
        CREATE INDEX audit_logs_resource_idx ON public.audit_logs(resource_type, resource_id);

        ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.knowledge_bases ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.usage_records ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.alembic_version ENABLE ROW LEVEL SECURITY;

        REVOKE ALL ON public.profiles, public.knowledge_bases, public.documents,
            public.conversations, public.messages, public.feedback,
            public.usage_records, public.audit_logs, public.alembic_version
            FROM anon, authenticated;
    """
    for statement in statements.split(";"):
        if statement.strip():
            op.execute(statement)


def downgrade() -> None:
    statements = """
        DROP TABLE public.audit_logs;
        DROP TABLE public.usage_records;
        DROP TABLE public.feedback;
        DROP TABLE public.messages;
        DROP TABLE public.conversations;
        DROP TABLE public.documents;
        DROP TABLE public.knowledge_bases;
        DROP TABLE public.profiles;
    """
    for statement in statements.split(";"):
        if statement.strip():
            op.execute(statement)
