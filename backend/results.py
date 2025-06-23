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
    quiz_name: str = Form(...),
    time_taken: int = Form(...),  # 👈 new field to accept time in seconds from frontend
    session: Session = Depends(get_session)
):
    # Decode JWT
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=403, detail="Invalid token.")
    user_uuid = user_data["sub"]

    user = session.exec(select(User).where(User.user_id == user_uuid)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    internal_user_id = user.id

    # Parse answers from JSON string
    answer_map: Dict[str, str] = json.loads(answers)

    # Fetch the quiz
    quiz = session.exec(select(Quiz).where(Quiz.quiz_name == quiz_name)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # Fetch questions for this quiz
    questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()

    # Calculate score
    score = 0
    for q in questions:
        qid = str(q.id)
        if qid in answer_map:
            user_ans = answer_map[qid].upper()
            correct_ans = ["A", "B", "C", "D"][q.correct_index]
            if user_ans == correct_ans:
                score += 1

    # Calculate accuracy
    total_questions = len(questions)
    accuracy = round((score / total_questions) * 100, 2) if total_questions else 0.0

    # Save result
    result = QuizResult(
        user_id=internal_user_id,
        quiz_id=quiz.id,
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,  # ⏱️ received from frontend
        finished_at=datetime.utcnow()
    )

    session.add(result)
    session.commit()

    return {
        "user_id": user_uuid,
        "quiz_name": quiz.quiz_name,
        "score": score,
        "total": total_questions,
        "accuracy": accuracy,
        "time_taken": time_taken
    }
