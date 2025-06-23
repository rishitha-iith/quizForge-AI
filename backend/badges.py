from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from models import QuizResult, User
from database import get_session

router = APIRouter()

@router.get("/badges/{user_identifier}")
def get_badges(user_identifier: str, session: Session = Depends(get_session)):
    # Try to get user by email or user_id (UUID)
    user = session.exec(
        select(User).where((User.email == user_identifier) | (User.user_id == user_identifier))
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Now use user.id (int) for querying QuizResult
    quizzes = session.exec(select(QuizResult).where(QuizResult.user_id == user.id)).all()

    total = len(quizzes)
    top_scorer = any(r.score == getattr(r, "total", r.score) for r in quizzes)  # fallback if no 'total' column
    fast_finisher = any(r.finished_at and r.finished_at.minute < 2 for r in quizzes if r.finished_at)

    badges = []
    if total >= 5:
        badges.append("Quiz Master")
    if top_scorer:
        badges.append("Top Scorer")
    if fast_finisher:
        badges.append("Fast Finisher")

    return {"user_id": user.user_id, "badges": badges}
