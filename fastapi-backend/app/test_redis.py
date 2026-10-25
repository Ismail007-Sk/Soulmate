from config.settings import settings
import redis.asyncio as redis
import asyncio

async def main():
    client = redis.from_url(
        settings.REDIS_URL,  # Use lowercase here
        decode_responses=True,
    )
    await client.set("test", "Soulmate is connected!")
    print(await client.get("test"))
    await client.aclose()

asyncio.run(main())