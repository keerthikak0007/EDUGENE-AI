from __future__ import annotations

import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(
    text: str
) -> str:

    text = text.strip()


    # Remove opening Markdown fence
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )


    # Remove closing Markdown fence
    text = re.sub(
        r"\s*```$",
        "",
        text
    )


    # Find JSON array
    start = text.find("[")

    end = text.rfind("]")


    if (
        start != -1
        and end != -1
        and end > start
    ):

        return text[
            start:end + 1
        ]


    return text


def _validate_quiz(
    data: Any
) -> list[dict[str, Any]]:

    if not isinstance(
        data,
        list
    ):

        raise ValueError(
            "Quiz response is not a JSON list."
        )


    validated = []


    for item in data[:3]:

        if not isinstance(
            item,
            dict
        ):

            continue


        question = str(
            item.get(
                "question",
                ""
            )
        ).strip()


        options = item.get(
            "options",
            []
        )


        answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip()


        if not question:

            continue


        if not isinstance(
            options,
            list
        ):

            continue


        if len(options) != 4:

            continue


        options = [
            str(option).strip()
            for option in options
        ]


        # Make sure options are unique
        if len(set(options)) != 4:

            continue


        # Answer must be one of options
        if answer not in options:

            # Allow A/B/C/D answers too
            if answer.upper() in {
                "A",
                "B",
                "C",
                "D"
            }:

                index = (
                    ord(answer.upper())
                    - ord("A")
                )

                answer = options[index]

            else:

                continue


        validated.append(
            {
                "question": question,
                "options": options,
                "answer": answer
            }
        )


    if not validated:

        raise ValueError(
            "Gemini did not return usable quiz questions."
        )


    return validated


def generate_quiz(
    text: str
) -> list[dict[str, Any]]:

    text = text.strip()


    if not text:

        raise ValueError(
            "Please provide text for the quiz."
        )


    prompt = f"""
You are a quiz generator.

Read the educational passage below.

Create exactly 3 multiple-choice questions.

Every question must contain:

- question
- exactly 4 options
- one correct answer

The answer must exactly match
one of the four options.

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option"
  }}
]

EDUCATIONAL PASSAGE:

{text}
"""


    raw = generate_text(

        prompt,

        system_instruction=(
            "You are a machine-readable quiz generator. "
            "Return valid JSON only."
        ),

        max_output_tokens=1500,

        json_mode=True
    )


    cleaned = clean_json_block(
        raw
    )


    try:

        data = json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Gemini returned invalid JSON: {exc}"
        ) from exc


    return _validate_quiz(
        data
    )