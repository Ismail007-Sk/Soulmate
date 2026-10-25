import logging
from google import genai
from google.genai import types
from app.config.settings import settings


logger = logging.getLogger(__name__)

EMBEDDING_DIMENSIONS = 768

client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        response = client.models.embed_content(
            model=settings.GEMINI_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=EMBEDDING_DIMENSIONS,
            ),
        )

        if not response.embeddings:
            raise ValueError("Gemini returned no embeddings.")

        embedding = response.embeddings[0].values

        if (
            embedding is None
            or len(embedding) != EMBEDDING_DIMENSIONS
        ):
            raise ValueError(
                f"Expected {EMBEDDING_DIMENSIONS} dimensions."
            )

        return embedding

    except Exception:
        logger.exception("Failed to generate text embedding.")
        raise