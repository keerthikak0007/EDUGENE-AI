from __future__ import annotations

from gemini_client import generate_text


def answer_question_with_gemini(
    question: str
) -> str:

    question = question.strip()


    if not question:

        raise ValueError(
            "Please provide a question."
        )


    return generate_text(

        question,

        system_instruction=(
            "You are EduGenie, an educational "
            "question-answering assistant. "

            "Answer clearly, accurately and "
            "in student-friendly language. "

            "Keep simple questions concise. "

            "For calculations or technical questions, "
            "show the important steps. "

            "If a question is ambiguous, clearly "
            "state the assumption you are making."
        ),

        max_output_tokens=900
    )