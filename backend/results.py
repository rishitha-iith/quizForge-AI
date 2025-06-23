from fastapi import APIRouter, Form, Depends, HTTPException
from sqlmodel import select, Session
from typing import Dict
from models import Question, Quiz, QuizResult, User
from utils import decode_access_token
from database import get_session
from datetime import datetime
import json

router = APIRouter()

@router.post("/submit_answers")
def submit_answers(
    token: str = Form(...),
    answers: str = Form(...),
    quiz_id: str = Form(...),
    time_taken: int = Form(...),
    session: Session = Depends(get_session)
):
    # 🔐 Decode token
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=403, detail="Invalid token.")
    user_uuid = user_data["sub"]

    user = session.exec(select(User).where(User.user_id == user_uuid)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # 📘 Get the quiz
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # 🚫 Check if user already submitted
    existing_result = session.exec(
        select(QuizResult).where((QuizResult.user_id == user.id) & (QuizResult.quiz_id == quiz.id))
    ).first()
    if existing_result:
        raise HTTPException(status_code=403, detail="You have already submitted this quiz.")

    # 📥 Parse answer map (key = question_id as str, value = "A"/"B"/"C"/"D")
    try:
        answer_map: Dict[str, str] = json.loads(answers)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid answers format.")

    # ✅ Fetch all questions
    questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()

    # 🧮 Calculate score
    score = 0
    for q in questions:
        qid_str = str(q.question_id)  # frontend uses question_id (not DB id)
        if qid_str in answer_map:
            user_ans = answer_map[qid_str].upper()
            correct_ans = ["A", "B", "C", "D"][q.correct_index]
            if user_ans == correct_ans:
                score += 1

    total_questions = len(questions)
    accuracy = round((score / total_questions) * 100, 2) if total_questions else 0.0

    # 💾 Store result
    result = QuizResult(
        user_id=user.id,
        quiz_id=quiz.id,
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,
        finished_at=datetime.utcnow()
    )
    session.add(result)
    session.commit()

    return {
        "status": "submitted",
        "user_id": user.user_id,
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "score": score,
        "total": total_questions,
        "accuracy": accuracy,
        "time_taken": time_taken
    }
