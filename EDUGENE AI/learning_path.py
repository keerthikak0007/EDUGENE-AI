from __future__ import annotations

from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    topic = topic.strip()


    if not topic:

        raise ValueError(
            "Please provide a topic."
        )


    prompt = f"""
You are an AI tutor.

The student wants to learn:

{topic}

Create a structured learning path.

Include:

1. Introduction
2. Beginner level
3. Intermediate level
4. Advanced level when appropriate
5. Important topics in learning order
6. Practical exercises
7. Mini-project ideas
8. Useful learning resources
9. Estimated time for each stage
10. Tips for improving understanding

Make the learning plan practical,
student-friendly and easy to follow.
"""


    return generate_text(

        prompt,

        system_instruction=(
            "You are EduGenie, a supportive "
            "learning-path planner for students."
        ),

        max_output_tokens=1800
    )