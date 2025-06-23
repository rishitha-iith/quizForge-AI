from fastapi import APIRouter, Depends
from sqlmodel import select, func, Session
from database import get_session
from models import QuizResult, User

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard(session: Session = Depends(get_session)):
    # Step 1: Get total score grouped by integer user ID (QuizResult.user_id is an int foreign key to User.id)
    data = session.exec(
        select(
            QuizResult.user_id,
            func.sum(QuizResult.score).label("score_sum")
        ).group_by(QuizResult.user_id)
        .order_by(func.sum(QuizResult.score).desc())
    ).all()

    # Step 2: Fetch username for each user_id using User.id
    leaderboard = []
    for user_id, total_score in data:
        user = session.exec(select(User).where(User.id == user_id)).first()  # use User.id (int)
        if user:
            leaderboard.append({
                "username": user.username,
                "score": total_score
            })

    return leaderboard
