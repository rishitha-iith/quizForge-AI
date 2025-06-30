from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlmodel import Session, select
import json, re, fitz, requests
from database import get_session
from models import Quiz, Question, UserQuiz, User
from typing import List, Union
from pydantic import BaseModel

router = APIRouter()

# 🔐 OpenRouter API Config
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

class QuestionIn(BaseModel):
    question: str
    options: List[str]
    correct_option: int


@router.post("/generate_quiz")
async def generate_quiz(
    user_id: str = Form(...),
    quiz_name: str = Form(...),
    num_questions: int = Form(...),
    num_users: int = Form(...),
    difficulty: str = Form("medium"),
    duration_minutes: Union[int, None] = Form(None),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 👤 Validate user
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # 🚫 Prevent duplicate quiz name
    if session.exec(select(Quiz).where(Quiz.quiz_name == quiz_name)).first():
        raise HTTPException(status_code=400, detail="Quiz name already exists.")

    # 📄 Read uploaded PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ''.join(page.get_text() for page in doc)

    # 🤖 Prompt for quiz generation
    prompt = f"""
You are an educational quiz generation assistant. Based on the text provided, generate {num_questions} multiple-choice questions (MCQs) of {difficulty} difficulty level. Each question must:
- Be relevant to the provided text.
- Contain 4 answer options labeled A, B, C, and D.
- Include a `correct_option` field (0 for A, 1 for B, etc.).
Return the output as a pure JSON array of objects with:
- `question`: string
- `options`: list of 4 strings
- `correct_option`: integer

Here is the text:
{text[:3000]}
"""

    # 📤 Call OpenRouter API to generate questions
    try:
        res = requests.post(
            OPENROUTER_URL,
            headers={
                'Authorization': f"Bearer {OPENROUTER_API_KEY}",
                'Content-Type': 'application/json'
            },
            json={
                'model': LLM_MODEL,
                'messages': [{'role': 'user', 'content': prompt}]
            }
        )
        res.raise_for_status()
        data = res.json()

        if "choices" not in data:
            raise ValueError(data.get("error", "Missing 'choices' in response."))

        content = data["choices"][0]["message"]["content"]
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if not match:
            raise ValueError("LLM response does not contain a JSON array.")

        questions_data = json.loads(match.group(0))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM failed: {e}")

    # ⏱️ Optional: Suggest quiz duration using AI
    if not duration_minutes:
        time_prompt = f"Suggest time in minutes for a {difficulty} quiz with {len(questions_data)} questions. Only return a number."

        try:
            res2 = requests.post(
                OPENROUTER_URL,
                headers={
                    'Authorization': f"Bearer {OPENROUTER_API_KEY}",
                    'Content-Type': 'application/json'
                },
                json={
                    'model': LLM_MODEL,
                    'messages': [{'role': 'user', 'content': time_prompt}]
                }
            )
            res2.raise_for_status()
            data2 = res2.json()
            if "choices" in data2:
                time_text = data2["choices"][0]["message"]["content"]
                suggested_time = int(re.search(r"\d+", time_text).group())
                duration_minutes = suggested_time
            else:
                duration_minutes = 10  # fallback
        except Exception:
            duration_minutes = 10  # fallback

    # 💾 Create quiz entry
    quiz = Quiz(
        quiz_name=quiz_name,
        max_users=num_users,
        creator_id=user.user_id,
        difficulty=difficulty,
        duration_minutes=duration_minutes
    )
    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    # 💾 Insert generated questions
    for q in questions_data:
        question = Question(
            quiz_id=quiz.quiz_id,
            question_text=q["question"],
            option_a=q["options"][0],
            option_b=q["options"][1],
            option_c=q["options"][2],
            option_d=q["options"][3],
            correct_index=q["correct_option"]
        )
        session.add(question)

    session.commit()

    # ✅ Response
    return {
        "status": "success",
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "difficulty": quiz.difficulty,
        "duration_minutes": quiz.duration_minutes,
        "participants_attempted": quiz.participants_attempted,
        "message": f"Created {len(questions_data)} questions"
    }
