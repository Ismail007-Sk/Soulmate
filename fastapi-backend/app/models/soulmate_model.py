import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class PersonalityType(str, Enum):
    CARING = "CARING"
    PLAYFUL = "PLAYFUL"
    HUMOROUS = "HUMOROUS"
    SARCASTIC = "SARCASTIC"
    EMPATHETIC = "EMPATHETIC"
    SUPPORTIVE = "SUPPORTIVE"
    INTELLECTUAL = "INTELLECTUAL"
    TEASING = "TEASING"
    CALM = "CALM"
    MOTIVATIONAL = "MOTIVATIONAL"
    CUTE_ANGRY = "CUTE_ANGRY"
    DRAMATIC = "DRAMATIC"
    SASSY = "SASSY"
    AFFECTIONATE = "AFFECTIONATE"
    MOCK_OFFENDED = "MOCK_OFFENDED"


class Language(str, Enum):
    ENGLISH = "ENGLISH"
    HINGLISH = "HINGLISH"
    BENGLISH = "BENGLISH"


class CommunicationStyle(str, Enum):
    CASUAL = "CASUAL"
    EXPRESSIVE = "EXPRESSIVE"
    WITTY = "WITTY"
    PLAYFUL = "PLAYFUL"
    GENTLE = "GENTLE"
    SARCASTIC = "SARCASTIC"
    DRAMATIC = "DRAMATIC"
    STRAIGHTFORWARD = "STRAIGHTFORWARD"
    TALKATIVE = "TALKATIVE"


class HumorRegion(str, Enum):
    WEST_BENGAL = "WEST_BENGAL"
    DELHI = "DELHI"


class Soulmate(Base):
    __tablename__ = "soulmates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        SAEnum(Gender, name="soulmate_gender"),
        nullable=False,
    )

    personality: Mapped[list[PersonalityType]] = mapped_column(
        ARRAY(SAEnum(PersonalityType, name="personality_type")),
        nullable=False,
    )

    language: Mapped[Language] = mapped_column(
        SAEnum(Language, name="soulmate_language"),
        nullable=False,
    )

    communication_style: Mapped[list[CommunicationStyle]] = mapped_column(
        ARRAY(
            SAEnum(
                CommunicationStyle,
                name="communication_style_type",
            )
        ),
        nullable=False,
    )

    humor_region: Mapped[HumorRegion] = mapped_column(
        SAEnum(HumorRegion, name="humor_region"),
        nullable=False,
        default=HumorRegion.WEST_BENGAL,
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
