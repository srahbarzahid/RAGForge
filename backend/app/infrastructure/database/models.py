"""Module 2 relational models. Supabase Auth remains identity owner."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
    UniqueConstraint,
    desc,
    func,
)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())

# Reference only. Migrations never create or modify Supabase-managed auth.users.
Table(
    "users",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    schema="auth",
    info={"external": True},
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    full_name = Column(Text)
    status = Column(Text, nullable=False, server_default="ACTIVE")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    __table_args__ = (
        CheckConstraint("length(btrim(name)) > 0"),
        CheckConstraint("chunk_target_tokens > 0"),
        CheckConstraint("chunk_max_tokens >= chunk_target_tokens"),
        CheckConstraint(
            "chunk_overlap_tokens >= 0 AND chunk_overlap_tokens < chunk_target_tokens"
        ),
        CheckConstraint("version > 0"),
        UniqueConstraint("id", "user_id"),
        Index("knowledge_bases_user_id_idx", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(Text, nullable=False, server_default="ACTIVE")
    embedding_provider = Column(Text)
    embedding_model = Column(Text)
    chunk_strategy = Column(Text)
    chunk_target_tokens = Column(Integer, nullable=False, server_default="500")
    chunk_max_tokens = Column(Integer, nullable=False, server_default="800")
    chunk_overlap_tokens = Column(Integer, nullable=False, server_default="75")
    version = Column(Integer, nullable=False, server_default="1")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        ForeignKeyConstraint(
            ["knowledge_base_id", "user_id"],
            ["knowledge_bases.id", "knowledge_bases.user_id"],
        ),
        CheckConstraint("size_bytes >= 0"),
        CheckConstraint(
            "status IN ('UPLOADED','QUEUED','PARSING','CHUNKING','EMBEDDING',"
            "'INDEXING','READY','FAILED','DELETING','DELETED')"
        ),
        CheckConstraint("version > 0"),
        CheckConstraint("page_count >= 0"),
        CheckConstraint("chunk_count >= 0"),
        UniqueConstraint("id", "user_id"),
        Index("documents_user_kb_idx", "user_id", "knowledge_base_id"),
        Index("documents_kb_status_idx", "knowledge_base_id", "status"),
        Index("documents_kb_user_idx", "knowledge_base_id", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    knowledge_base_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(Text, nullable=False)
    original_filename = Column(Text, nullable=False)
    mime_type = Column(Text, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    storage_key = Column(Text, nullable=False, unique=True)
    checksum = Column(Text, nullable=False)
    status = Column(Text, nullable=False, server_default="UPLOADED")
    version = Column(Integer, nullable=False, server_default="1")
    is_active = Column(Boolean, nullable=False, server_default="true")
    page_count = Column(Integer)
    chunk_count = Column(Integer)
    processing_error = Column(Text)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    deleted_at = Column(DateTime(timezone=True))


class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = (
        ForeignKeyConstraint(
            ["knowledge_base_id", "user_id"],
            ["knowledge_bases.id", "knowledge_bases.user_id"],
        ),
        UniqueConstraint("id", "user_id"),
        Index("conversations_user_activity_idx", "user_id", desc("last_activity_at")),
        Index("conversations_kb_idx", "knowledge_base_id"),
        Index("conversations_kb_user_idx", "knowledge_base_id", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    knowledge_base_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(Text)
    status = Column(Text, nullable=False, server_default="ACTIVE")
    started_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_activity_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        ForeignKeyConstraint(
            ["conversation_id", "user_id"],
            ["conversations.id", "conversations.user_id"],
        ),
        CheckConstraint("role IN ('user','assistant','system','tool')"),
        CheckConstraint("input_tokens >= 0"),
        CheckConstraint("output_tokens >= 0"),
        CheckConstraint("latency_ms >= 0"),
        UniqueConstraint("id", "user_id"),
        Index("messages_conversation_created_idx", "conversation_id", "created_at"),
        Index("messages_user_id_idx", "user_id"),
        Index("messages_conversation_user_idx", "conversation_id", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), nullable=False)
    role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    model = Column(Text)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    latency_ms = Column(Integer)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        ForeignKeyConstraint(
            ["message_id", "user_id"], ["messages.id", "messages.user_id"]
        ),
        CheckConstraint("rating BETWEEN 1 AND 5"),
        UniqueConstraint("user_id", "message_id"),
        Index("feedback_message_id_idx", "message_id"),
        Index("feedback_message_user_idx", "message_id", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    message_id = Column(UUID(as_uuid=True), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class UsageRecord(Base):
    __tablename__ = "usage_records"
    __table_args__ = (
        CheckConstraint("input_tokens >= 0"),
        CheckConstraint("output_tokens >= 0"),
        CheckConstraint("embedding_tokens >= 0"),
        CheckConstraint("latency_ms >= 0"),
        CheckConstraint("estimated_cost >= 0"),
        Index("usage_records_user_created_idx", "user_id", desc("created_at")),
        Index("usage_records_kb_idx", "knowledge_base_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="SET NULL")
    )
    knowledge_base_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id"))
    request_type = Column(Text, nullable=False)
    input_tokens = Column(Integer, nullable=False, server_default="0")
    output_tokens = Column(Integer, nullable=False, server_default="0")
    embedding_tokens = Column(Integer, nullable=False, server_default="0")
    latency_ms = Column(Integer)
    estimated_cost = Column(Numeric(18, 8))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("audit_logs_user_created_idx", "user_id", desc("created_at")),
        Index("audit_logs_resource_idx", "resource_type", "resource_id"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="SET NULL")
    )
    action = Column(Text, nullable=False)
    resource_type = Column(Text, nullable=False)
    resource_id = Column(UUID(as_uuid=True))
    metadata_ = Column("metadata", JSONB, nullable=False, server_default="{}")
    ip_address = Column(INET)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
