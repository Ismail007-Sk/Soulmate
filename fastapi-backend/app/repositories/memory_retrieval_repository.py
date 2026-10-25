import uuid
from sqlalchemy.orm import Session
from app.models.memory_model import Memory


def retrieve_relevant_memories(
    db: Session,
    user_id: uuid.UUID,
    query_embedding: list[float],
    limit: int = 5,
) -> list[Memory]:
    """
    Retrieve the most relevant memories belonging to a specific user
    using cosine distance.
    """
    if not query_embedding:
        return []

    if limit <= 0:
        return []

    return (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.embedding.is_not(None),
        )
        .order_by(Memory.embedding.cosine_distance(query_embedding))
        .limit(limit)
        .all()
    )
