import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.soulmate_model import (
    CommunicationStyle,
    Gender,
    HumorRegion,
    Language,
    PersonalityType,
)


class SoulmateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    gender: Gender
    personality: list[PersonalityType] = Field(min_length=1)
    language: Language
    communication_style: list[CommunicationStyle] = Field(min_length=1)
    humor_region: HumorRegion = HumorRegion.WEST_BENGAL

class SoulmateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    gender: Gender | None = None
    personality: list[PersonalityType] | None = Field(default=None, min_length=1)
    language: Language | None = None
    communication_style: list[CommunicationStyle] | None = Field(
        default=None,
        min_length=1,
    )
    humor_region: HumorRegion | None = None

class SoulmateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    gender: Gender
    personality: list[PersonalityType]
    language: Language
    communication_style: list[CommunicationStyle]
    humor_region: HumorRegion
    created_at: datetime
    updated_at: datetime
