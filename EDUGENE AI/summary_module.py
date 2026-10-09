from __future__ import annotations

from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    text = text.strip()


    if not text:

        raise ValueError(
            "Please provide text to summarize."
        )


    prompt = f"""
Summarize the following educational text.

Requirements:

1. Keep the important information.
2. Remove unnecessary repetition.
3. Use simple language.
4. Keep important facts and concepts.
5. Use short paragraphs or bullet points where helpful.

TEXT:

{text}
"""


    return generate_text(

        prompt,

        system_instruction=(
            "You are EduGenie, an educational "
            "summarization assistant."
        ),

        max_output_tokens=900
    )