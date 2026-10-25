import asyncio
import logging
from app.config.database import SessionLocal
from app.config.redis import redis_client
from app.services.memory_service import process_user_memories

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 300  # 5 minutes


async def memory_worker():
    while True:
        try:
            # Find users who have pending chat messages
            keys = await redis_client.keys("chat:*:user_messages")

            for key in keys:
                try:
                    # Extract user ID from Redis key
                    user_id = key.split(":")[1]

                    # Process messages using a database session
                    db = SessionLocal()
                    try:
                        await process_user_memories(db, user_id)
                    finally:
                        db.close()

                except Exception:
                    logger.exception(
                        "Memory extraction failed for key %s",
                        key,
                    )

        except Exception:
            logger.exception("Memory worker iteration failed")

        await asyncio.sleep(INTERVAL_SECONDS)
