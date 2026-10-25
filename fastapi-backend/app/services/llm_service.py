import httpx
from fastapi import HTTPException, status
from app.config.settings import settings


def generate_reply(messages: list[dict[str, str]]) -> str:
    try:
        response = httpx.post(
            f"{settings.GROQ_BASE_URL.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GROQ_MODEL,
                "messages": messages,
                "temperature": 0.3,
            },
            timeout=60.0,
        )
        response.raise_for_status()

    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The LLM provider timed out.",
        ) from exc

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The LLM provider returned an error.",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not connect to the LLM provider.",
        ) from exc

    try:
        reply = response.json()["choices"][0]["message"]["content"]

    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The LLM provider returned an invalid response.",
        ) from exc

    if not isinstance(reply, str) or not reply.strip():
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The LLM provider returned an empty response.",
        )

    return reply.strip()
