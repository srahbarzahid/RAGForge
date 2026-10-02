"""Cover composite ownership foreign keys with indexes.

Revision ID: 20261002_02
Revises: 20261002_01
"""

from alembic import op

revision = "20261002_02"
down_revision = "20261002_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "documents_kb_user_idx", "documents", ["knowledge_base_id", "user_id"]
    )
    op.create_index(
        "conversations_kb_user_idx", "conversations", ["knowledge_base_id", "user_id"]
    )
    op.create_index(
        "messages_conversation_user_idx", "messages", ["conversation_id", "user_id"]
    )
    op.create_index("feedback_message_user_idx", "feedback", ["message_id", "user_id"])


def downgrade() -> None:
    op.drop_index("feedback_message_user_idx", table_name="feedback")
    op.drop_index("messages_conversation_user_idx", table_name="messages")
    op.drop_index("conversations_kb_user_idx", table_name="conversations")
    op.drop_index("documents_kb_user_idx", table_name="documents")
