import logging
import uuid
from sqlalchemy.orm import Session
from app.config.redis import redis_client
from app.repositories.memory_repository import create_memories
from app.services.memory_extraction_service import extract_memories

logger = logging.getLogger(__name__)

BATCH_SIZE = 10


async def process_user_memories(
    db: Session,
    user_id: uuid.UUID,
) -> int:
    chat_key = f"chat:{user_id}:user_messages"

    # 1. Retrieve up to 10 unprocessed user messages.
    messages = await redis_client.lrange(
        chat_key,
        0,
        BATCH_SIZE - 1,
    )

    if not messages:
        return 0

    try:
        # 2. Extract relevant memories using the LLM.
        memories = extract_memories(messages)

        # 3. Generate embeddings and save memories to PostgreSQL.
        # The repository handles embedding generation and persistence.
        saved_memories = create_memories(
            db=db,
            user_id=user_id,
            memories=memories[:BATCH_SIZE],
        )

        # 4. Verify that the batch has not changed.
        current_messages = await redis_client.lrange(
            chat_key,
            0,
            len(messages) - 1,
        )

        if current_messages != messages:
            logger.warning(
                "Redis message batch changed for user %s; "
                "messages were retained.",
                user_id,
            )
            return len(saved_memories)

        # 5. Remove the processed messages.
        await redis_client.ltrim(
            chat_key,
            len(messages),
            -1,
        )

        logger.info(
            "Processed %s messages and saved %s memories for user %s",
            len(messages),
            len(saved_memories),
            user_id,
        )

        return len(saved_memories)

    except Exception:
        logger.exception(
            "Memory processing failed for user %s; messages retained.",
            user_id,
        )
        raise