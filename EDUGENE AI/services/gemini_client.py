from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiConfigurationError(RuntimeError):
    """
    Raised when Gemini API configuration is missing.
    """
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:

    if not GEMINI_API_KEY:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )
def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    max_output_tokens: int = 1024,
    json_mode: bool = False,
) -> str:

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    config_kwargs = {
        "max_output_tokens": max_output_tokens
    }

    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction

    if json_mode:
        config_kwargs["response_mime_type"] = "application/json"

    config = types.GenerateContentConfig(
        **config_kwargs
    )

    client = get_client()

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=config,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as e:
            last_error = e

            if "503" in str(e) or "UNAVAILABLE" in str(e):
                import time
                time.sleep(2 ** attempt)
                continue

            raise

    raise RuntimeError(
        f"Gemini is temporarily unavailable after 3 attempts: {last_error}"
    )