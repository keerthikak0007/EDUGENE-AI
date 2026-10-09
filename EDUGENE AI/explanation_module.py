from __future__ import annotations

from config import (
    LOCAL_EXPLANATION_MODEL,
    USE_LOCAL_EXPLANATION,
)

from gemini_client import generate_text


def _local_explain(
    topic: str
) -> str:

    from transformers import (
        AutoModelForSeq2SeqLM,
        AutoTokenizer,
    )


    tokenizer = AutoTokenizer.from_pretrained(
        LOCAL_EXPLANATION_MODEL
    )


    model = AutoModelForSeq2SeqLM.from_pretrained(
        LOCAL_EXPLANATION_MODEL
    )


    prompt = (
        f"Explain the concept of '{topic}' "
        "in a simple and clear way for a school student."
    )


    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )


    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )


    explanation = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


    return explanation.strip()


def explain_topic(
    topic: str
) -> str:

    topic = topic.strip()


    if not topic:

        raise ValueError(
            "Please provide a topic."
        )


    # Optional local model
    if USE_LOCAL_EXPLANATION:

        try:

            return _local_explain(topic)

        except Exception:

            # If local model fails,
            # automatically use Gemini.
            pass


    # Gemini explanation
    return generate_text(

        f"""
Explain the concept of '{topic}'.

Requirements:

1. Use simple student-friendly language.
2. Explain the meaning clearly.
3. Break difficult ideas into small parts.
4. Give one simple example when useful.
5. Avoid unnecessary technical jargon.
6. Make the explanation easy to study.
""",

        system_instruction=(
            "You are EduGenie, a patient AI tutor. "
            "Your job is to explain concepts accurately "
            "and simply for students."
        ),

        max_output_tokens=700
    )