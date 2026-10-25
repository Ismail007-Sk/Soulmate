import uuid
from sqlalchemy.orm import Session
from app.models.memory_model import Memory
from app.schemas.memory_schema import MemoryExtraction
from app.services.embedding_service import generate_embedding


def create_memories(
    db: Session,
    user_id: uuid.UUID,
    memories: list[MemoryExtraction],
) -> list[Memory]:
    if not memories:
        return []

    try:
        db_memories = []

        for memory in memories:
            if not memory.is_relevant:
                continue

            embedding = generate_embedding(memory.memory_text)

            db_memory = Memory(
                user_id=user_id,
                memory_text=memory.memory_text,
                category=memory.category,
                event_at=memory.event_at,
                embedding=embedding,
            )

            db_memories.append(db_memory)

        if not db_memories:
            return []

        db.add_all(db_memories)
        db.commit()

        for memory in db_memories:
            db.refresh(memory)

        return db_memories

    except Exception:
        db.rollback()
        raise