import enum
import uuid
from datetime import datetime
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class MemoryCategory(str, enum.Enum):
    PERSONAL_INFO = "PERSONAL_INFO"
    PREFERENCE = "PREFERENCE"
    HOBBY = "HOBBY"
    RELATIONSHIP = "RELATIONSHIP"
    LIFE_EVENTS = "LIFE_EVENTS"
    UPCOMING_EVENT = "UPCOMING_EVENT"
    OTHERS = "OTHERS"


class Memory(Base):
    __tablename__ = "memories"

    __table_args__ = (
        CheckConstraint(
            """
            (
                category = 'UPCOMING_EVENT'
                AND event_at IS NOT NULL
            )
            OR
            (
                category != 'UPCOMING_EVENT'
                AND event_at IS NULL
            )
            """,
            name="ck_memories_event_at_category",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    memory_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768),
        nullable=True,
    )

    category: Mapped[MemoryCategory] = mapped_column(
        Enum(MemoryCategory, name="memory_category"),
        nullable=False,
    )

    event_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )