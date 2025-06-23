# backend/quiz.py

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
    # Decode and verify token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token.")
    uuid_sub = payload["sub"]

    user_obj = session.exec(select(User).where(User.user_id == uuid_sub)).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found.")
    user_pk = user_obj.id

    # Validate PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ''.join(page.get_text() for page in doc)

    # Create prompt for questions
    prompt = f"""
You are an educational quiz generation assistant. Based on the text provided, generate {num_questions} multiple-choice questions (MCQs) of **{difficulty}** difficulty level. Each question must:

- Be relevant to the provided text.
- Contain 4 answer options labeled A, B, C, and D.
- Include a `correct_option` field which is an integer (0 for option A, 1 for B, etc.).
- Be concise and clear (no vague or overly complex questions).
- Be accurate and factually correct.
- Return the output as a **pure JSON array** of objects, with each object containing:
  - `question`: string
  - `options`: list of 4 strings
  - `correct_option`: integer (0 to 3)

Do not include explanations or commentary. Only return the JSON array.

Here is the input text (truncated to the first 3000 characters for brevity):
{text[:3000]}
"""


    try:
        res = requests.post(
            os.getenv('OPENROUTER_URL'),
            headers={
                'Authorization': f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                'Content-Type': 'application/json'
            },
            json={ 'model': 'deepseek/deepseek-r1-0528-qwen3-8b:free', 'messages': [{'role':'user','content':prompt}] }
        )
        res.raise_for_status()
        raw = res.json()['choices'][0]['message']['content']
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if not match:
            raise ValueError("Unexpected LLM response format")
        questions_data = json.loads(match.group(0))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {e}")

    # 🧠 AI-Suggested Duration (if user didn't provide)
    if duration_minutes is None:
        duration_prompt = f"""Suggest a reasonable quiz time in minutes for a quiz with {len(questions_data)} questions at {difficulty} difficulty.
Only return an integer."""
        try:
            res2 = requests.post(
                os.getenv('OPENROUTER_URL'),
                headers={
                    'Authorization': f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    'Content-Type': 'application/json'
                },
                json={ 'model': 'deepseek/deepseek-r1-0528-qwen3-8b:free', 'messages': [{'role':'user','content':duration_prompt}] }
            )
            res2.raise_for_status()
            suggested_time = int(re.search(r"\d+", res2.json()['choices'][0]['message']['content']).group())
            duration_minutes = suggested_time
        except Exception as e:
            duration_minutes = 10  # fallback default

    # Create quiz
    quiz = Quiz(
        quiz_name=quiz_name,
        max_users=num_users,
        creator_id=user_pk,
        difficulty=difficulty,
        duration_minutes=duration_minutes
    )
    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    # Save questions
    for q in questions_data:
        session.add(Question(
            quiz_id=quiz.id,
            question_text=q['question'],
            option_a=q['options'][0], option_b=q['options'][1],
            option_c=q['options'][2], option_d=q['options'][3],
            correct_index=q['correct_option']
        ))
    session.commit()

    # Add creator to participants
    session.add(UserQuiz(user_id=user_pk, quiz_id=quiz.id))
    session.commit()

    return {
        'status': 'success',
        'quiz_id': quiz.quiz_id,
        'quiz_name': quiz.quiz_name,
        'duration_minutes': quiz.duration_minutes,
        'difficulty': quiz.difficulty,
        'message': f"Created {len(questions_data)} questions"
    }
