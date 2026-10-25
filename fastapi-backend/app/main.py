from fastapi import FastAPI
from app.routers import auth_router, user_router, soulmate_router, chat_router
import asyncio
from contextlib import asynccontextmanager
from app.workers.memory_worker import memory_worker

# Worker
@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_task = asyncio.create_task(memory_worker())

    yield

    worker_task.cancel()

    try:
        await worker_task
    except asyncio.CancelledError:
        pass



app = FastAPI(
    title="Soulmate API",
    description="Backend API for the Soulmate AI companion application.",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers with the prefix argument
app.include_router(auth_router.authRouter, prefix="/api/v1")
app.include_router(user_router.userRouter, prefix="/api/v1")
app.include_router(soulmate_router.soulRouter, prefix="/api/v1")
app.include_router(chat_router.chatRouter, prefix="/api/v1")



@app.get("/", tags=["Health"])
def health_check():
    return {"message": "Soulmate API is running"}
