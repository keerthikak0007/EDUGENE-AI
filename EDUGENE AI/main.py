from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from services.gemini_client import generate_text


app = FastAPI(title="EduGenie AI")

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "frontend")),
    name="static"
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie AI"
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "EduGenie AI is running successfully!"
    }


# 👇 INDHA PART-A MAIN.PY LA PODANUM
@app.get("/qa")
async def ask_question(question: str):

    try:
        answer = generate_text(
            prompt=question,
            system_instruction=(
                "You are EduGenie, an educational AI assistant. "
                "Give clear, simple, accurate and helpful answers "
                "that are easy for students to understand."
            ),
            max_output_tokens=1024
        )

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        return {
            "question": question,
            "answer": "Sorry, I could not generate an answer.",
            "error": str(e)
        }