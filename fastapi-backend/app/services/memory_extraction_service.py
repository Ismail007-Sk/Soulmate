import json
from fastapi import HTTPException, status
from pydantic import ValidationError
from app.schemas.memory_schema import MemoryExtraction
from app.services.llm_service import generate_reply


def extract_memories(messages: list[str]) -> list[MemoryExtraction]:
    if not messages:
        return []

    conversation = "\n".join(
        f"{index}. {message}"
        for index, message in enumerate(messages, start=1)
    )


    prompt = f"""
    You are a memory extraction system for an AI companion.

    Analyze the following user messages and extract information
    worth remembering for future conversations.

    Rules:
    - Extract only useful, user-specific information.
    - Ignore casual greetings, temporary small talk, and irrelevant content.
    - Extract multiple distinct memories when appropriate.
    - Do not invent, assume, or infer facts not explicitly supported by the messages.
    - Assign exactly one category to each memory.
    - Write every memory_text in clear, concise English, regardless of the
    original language (Bengali, Benglish, Hindi, or English).
    - Translate and preserve the original meaning accurately.
    - Preserve names, dates, places, preferences, and important details.
    - Use UPCOMING_EVENT only for future events with a known date or time.
    - Use ISO 8601 format for event_at when the date/time is available.
    - If the timezone is unknown, do not invent one.
    - For all categories except UPCOMING_EVENT, event_at must be null.
    - If no useful information is found, return an empty memories list.
    - Return no more than 10 memories.

    Allowed categories:
    PERSONAL_INFO, PREFERENCE, HOBBY, RELATIONSHIP,
    LIFE_EVENTS, UPCOMING_EVENT, OTHERS.

    Return only valid JSON in this format:
    {{
        "memories": [
            {{
                "is_relevant": true,
                "memory_text": "The user enjoys animated movies.",
                "category": "HOBBY",
                "event_at": null
            }}
        ]
    }}

    Messages:
    {conversation}
    """.strip()

    try:
        response = generate_reply([
            {
                "role": "system",
                "content": (
                    "Extract user memories accurately. "
                    "Return valid JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ])

        data = json.loads(response)
        raw_memories = data["memories"]

        if not isinstance(raw_memories, list):
            raise ValueError("'memories' must be a list.")

        memories = []

        for item in raw_memories:
            memory = MemoryExtraction.model_validate(item)

            if memory.is_relevant:
                memories.append(memory)

        return memories

    except (json.JSONDecodeError, KeyError, TypeError, ValueError,
            ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The LLM returned an invalid memory extraction response.",
        ) from exc
