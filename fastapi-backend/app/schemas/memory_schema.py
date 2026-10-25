from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.memory_model import MemoryCategory


class MemoryExtraction(BaseModel):
    is_relevant: bool
    memory_text: str | None = Field(default=None, min_length=1)
    category: MemoryCategory | None = None
    event_at: datetime | None = None

    @model_validator(mode="after")
    def validate_memory(self):
        if self.is_relevant:
            if not self.memory_text or not self.memory_text.strip():
                raise ValueError(
                    "Relevant memories must have memory_text."
                )

            if self.category is None:
                raise ValueError(
                    "Relevant memories must have a category."
                )

            if self.category == MemoryCategory.UPCOMING_EVENT:
                if self.event_at is None:
                    raise ValueError(
                        "Upcoming events must have event_at."
                    )
            elif self.event_at is not None:
                raise ValueError(
                    "event_at is only allowed for UPCOMING_EVENT."
                )

        return self


class MemoryResponse(BaseModel):
    id: str
    user_id: str
    memory_text: str
    category: MemoryCategory
    event_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)