# backend/get_quiz.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Quiz, Question, UserQuiz, User
from datetime import datetime

router = APIRouter()

@router.get("/get_quiz/{quiz_code}/{user_id}")
def get_quiz_by_code(quiz_code: str, user_id: str, session: Session = Depends(get_session)):
    # Get the quiz
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_code)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Check current participants
    participant_count = session.exec(
        select(UserQuiz).where(UserQuiz.quiz_id == quiz.id)
    ).all()

    if len(participant_count) >= quiz.max_users:
        raise HTTPException(status_code=403, detail="Max participants limit reached")

    # Check if user is already registered
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_entry = session.exec(
        select(UserQuiz).where((UserQuiz.quiz_id == quiz.id) & (UserQuiz.user_id == user.id))
    ).first()

    # Register user in UserQuiz if not already
    if not existing_entry:
        user_quiz = UserQuiz(user_id=user.id, quiz_id=quiz.id)
        session.add(user_quiz)
        session.commit()

    # Get questions
    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz.id)
    ).all()

    question_data = [
        {
            "question_id": q.id,
            "question": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d]
        }
        for q in questions
    ]

    return {
        "quiz_name": quiz.quiz_name,
        "quiz_code": quiz.quiz_id,
        "difficulty": quiz.difficulty,  # NEW
        "duration_minutes": quiz.duration_minutes,  # NEW
        "questions": question_data,
        "max_users": quiz.max_users,
        "current_participants": len(participant_count)
    }
