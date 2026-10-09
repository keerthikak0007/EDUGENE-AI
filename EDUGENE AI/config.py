from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# Project directory
BASE_DIR = Path(__file__).resolve().parent


# Load .env file
load_dotenv(BASE_DIR / ".env")


# -----------------------------
# Application Settings
# -----------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "EduGenie"
)


HOST = os.getenv(
    "HOST",
    "127.0.0.1"
)


PORT = int(
    os.getenv(
        "PORT",
        "8000"
    )
)


# -----------------------------
# Gemini Settings
# -----------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# -----------------------------
# Local Explanation Model
# -----------------------------

USE_LOCAL_EXPLANATION = (
    os.getenv(
        "USE_LOCAL_EXPLANATION",
        "false"
    ).lower()
    == "true"
)


LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


# -----------------------------
# Input Limits
# -----------------------------

MAX_QUESTION_CHARS = int(
    os.getenv(
        "MAX_QUESTION_CHARS",
        "4000"
    )
)


MAX_TOPIC_CHARS = int(
    os.getenv(
        "MAX_TOPIC_CHARS",
        "500"
    )
)


MAX_TEXT_CHARS = int(
    os.getenv(
        "MAX_TEXT_CHARS",
        "20000"
    )
)