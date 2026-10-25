import logging
import uuid
from sqlalchemy.orm import Session
from app.repositories.memory_retrieval_repository import (
    retrieve_relevant_memories,
)
from app.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)

DEFAULT_MEMORY_LIMIT = 5


def retrieve_user_memories(
    db: Session,
    user_id: uuid.UUID,
    query: str,
    limit: int = DEFAULT_MEMORY_LIMIT,
) -> list[str]:
    """
    Generate a query embedding and retrieve relevant memories
    belonging exclusively to the specified user.
    """
    if not query or not query.strip():
        return []

    try:
        query_embedding = generate_embedding(
            text=query,
            task_type="RETRIEVAL_QUERY",
        )

        memories = retrieve_relevant_memories(
            db=db,
            user_id=user_id,
            query_embedding=query_embedding,
            limit=limit,
        )

        return [memory.memory_text for memory in memories]

    except Exception:
        logger.exception(
            "Failed to retrieve memories for user %s",
            user_id,
        )
        return []
