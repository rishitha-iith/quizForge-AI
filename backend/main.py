# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Dict
from sqlmodel import SQLModel, create_engine, Session, select
from uuid import uuid4
import fitz  # PyMuPDF
import json
import requests
import re
import os
from datetime import datetime
from dotenv import load_dotenv

from models import User, QuizResult, QuestionModel
from database import get_session, create_db_and_tables
from utils import hash_password, verify_password

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ----------- MODELS ------------
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Question(BaseModel):
    question: str
    options: List[str]
    correct_index: int

class Quiz(BaseModel):
    title: str
    questions: List[Question]

class UserResponse(BaseModel):
    user_id: str
    quiz_id: int
    answers: Dict[int, str]
    time_taken: int

# ---------- AUTH API ----------
@app.post("/signup")
def signup(user: SignupRequest):
    session = get_session()
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        user_id=str(uuid4()),
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"user_id": new_user.user_id}

@app.post("/login")
def login(identifier: str = Form(...), password: str = Form(...)):
    session = get_session()
    user = session.exec(select(User).where((User.email == identifier) | (User.username == identifier))).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": user.user_id, "username": user.username}

# ---------- QUIZ GENERATION ----------
@app.post("/generate_quiz", response_model=Quiz)
async def generate_quiz(
    user_id: str = Form(...),
    num_questions: int = Form(...),
    num_users: int = Form(...),
    pdf_file: UploadFile = File(...)
):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    content = await pdf_file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    prompt = f"""
    Generate {num_questions} multiple-choice questions from the following text.
    Each must have 4 options and a correct_option (0-based index).
    Return a pure JSON array like:
    [{{"question": "...", "options": ["A", "B", "C", "D"], "correct_option": 2}}, ...]
    Text: {text[:3000]}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quizforge-ai.onrender.com",
            "X-Title": "QuizForge AI",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
            "messages": [{"role": "user", "content": prompt}]
        })
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"LLM Error: {response.text}")

    raw_output = response.json()["choices"][0]["message"]["content"]
    match = re.search(r"\[\s*{.*}\s*]", raw_output, re.DOTALL)
    if not match:
        raise HTTPException(status_code=500, detail=f"Invalid response: {raw_output}")

    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON error: {str(e)}")

    session = get_session()
    questions = []
    for q in parsed:
        question_obj = QuestionModel(
            user_id=user_id,
            question=q['question'],
            options=json.dumps(q['options']),
            correct_index=q['correct_option']
        )
        session.add(question_obj)
        questions.append(Question(
            question=q['question'],
            options=q['options'],
            correct_index=q['correct_option']
        ))
    session.commit()

    return Quiz(title=pdf_file.filename.replace(".pdf", ""), questions=questions)

@app.get("/get_quiz", response_model=List[Question])
def get_quiz(user_id: str):
    session = get_session()
    results = session.exec(select(QuestionModel).where(QuestionModel.user_id == user_id)).all()
    return [
        Question(
            question=q.question,
            options=json.loads(q.options),
            correct_index=q.correct_index
        ) for q in results
    ]

@app.post("/submit_answers", response_model=UserResponse)
def submit_answers(user_id: str = Form(...), answers: str = Form(...)):
    session = get_session()
    try:
        answer_map = json.loads(answers)
    except:
        raise HTTPException(status_code=400, detail="Invalid answers format")

    results = session.exec(select(QuestionModel).where(QuestionModel.user_id == user_id)).all()
    score = 0
    for i, ans in answer_map.items():
        i = int(i)
        q = results[i]
        correct_letter = chr(65 + q.correct_index)
        if ans.upper() == correct_letter:
            score += 1

    new_result = QuizResult(
        user_id=user_id,
        quiz_name=f"Quiz-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        score=score,
        total=len(results),
        timestamp=datetime.now().isoformat()
    )
    session.add(new_result)
    session.commit()

    return UserResponse(user_id=user_id, quiz_id=1, answers=answer_map, time_taken=0)

@app.get("/leaderboard")
def leaderboard():
    session = get_session()
    from sqlmodel import func
    query = (
        session.query(
            QuizResult.user_id,
            func.sum(QuizResult.score).label("total_score")
        )
        .group_by(QuizResult.user_id)
        .order_by(func.sum(QuizResult.score).desc())
        .all()
    )

    results = []
    for user_id, total_score in query:
        user = session.exec(select(User).where(User.user_id == user_id)).first()
        results.append({
            "username": user.username if user else "Unknown",
            "user_id": user_id,
            "total_score": total_score
        })
    return results