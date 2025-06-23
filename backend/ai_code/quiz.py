from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlmodel import Session, select
import os, json, re, fitz, requests
from database import get_session
from models import Quiz, Question, UserQuiz, User
from utils import decode_access_token
from typing import List
from pydantic import BaseModel

router = APIRouter()

class QuestionIn(BaseModel):
    question: str
    options: List[str]
    correct_option: int

@router.post("/generate_quiz")
async def generate_quiz(
    token: str = Form(...),
    quiz_name: str = Form(...),
    num_questions: int = Form(...),
    num_users: int = Form(...),
    difficulty: str = Form("medium"),
    duration_minutes: int = Form(None),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token.")
    user_id = payload["sub"]

    # Get user
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # ⛔ Check for duplicate quiz name
    existing_quiz = session.exec(select(Quiz).where(Quiz.quiz_name == quiz_name)).first()
    if existing_quiz:
        raise HTTPException(status_code=400, detail="Quiz name already exists. Please choose another name.")

    # 🧾 Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ''.join(page.get_text() for page in doc)

    # 🧠 LLM Question Generation Prompt
    prompt = f"""
You are an educational quiz generation assistant. Based on the text provided, generate {num_questions} multiple-choice questions (MCQs) of **{difficulty}** difficulty level. Each question must:
- Be relevant to the provided text.
- Contain 4 answer options labeled A, B, C, and D.
- Include a `correct_option` field (0 for A, 1 for B, etc.).
- Return the output as a pure JSON array of objects with:
  - `question`: string
  - `options`: list of 4 strings
  - `correct_option`: integer

Here is the text:
{text[:3000]}
"""

    try:
        res = requests.post(
            os.getenv('OPENROUTER_URL'),
            headers={
                'Authorization': f"Bearer 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",
                'Content-Type': 'application/json'
            },
            json={'model': 'deepseek/deepseek-r1-0528-qwen3-8b:free', 'messages': [{'role': 'user', 'content': prompt}]}
        )
        res.raise_for_status()
        raw = res.json()['choices'][0]['message']['content']
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if not match:
            raise ValueError("Unexpected LLM response format")
        questions_data = json.loads(match.group(0))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {e}")

    # 🧠 AI-Suggested Time (fallback)
    if duration_minutes is None:
        time_prompt = f"Suggest time in minutes for a {difficulty} quiz with {len(questions_data)} questions. Only return a number."
        try:
            res2 = requests.post(
                os.getenv('OPENROUTER_URL'),
                headers={
                    'Authorization': f"Bearer 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",
                    'Content-Type': 'application/json'
                },
                json={'model': 'deepseek/deepseek-r1-0528-qwen3-8b:free', 'messages': [{'role': 'user', 'content': time_prompt}]}
            )
            res2.raise_for_status()
            suggested_time = int(re.search(r"\d+", res2.json()['choices'][0]['message']['content']).group())
            duration_minutes = suggested_time
        except Exception:
            duration_minutes = 10  # fallback

    # 📝 Create quiz
    quiz = Quiz(
        quiz_name=quiz_name,
        max_users=num_users,
        creator_id=user.id,
        difficulty=difficulty,
        duration_minutes=duration_minutes
    )
    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    # 💾 Add questions with manual question_id starting from 0
    for idx, q in enumerate(questions_data):
        question = Question(
            quiz_id=quiz.id,
            question_id=idx,
            question_text=q['question'],
            option_a=q['options'][0],
            option_b=q['options'][1],
            option_c=q['options'][2],
            option_d=q['options'][3],
            correct_index=q['correct_option']
        )
        session.add(question)

    session.commit()

    # 👤 Add creator as participant
    session.add(UserQuiz(user_id=user.id, quiz_id=quiz.id))
    session.commit()

    return {
        "status": "success",
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "difficulty": quiz.difficulty,
        "duration_minutes": quiz.duration_minutes,
        "message": f"Created {len(questions_data)} questions"
    }
