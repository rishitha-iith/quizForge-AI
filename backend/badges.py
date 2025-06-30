from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session, desc
from models import UserBadge
from database import get_session
from typing import Optional, Dict, List

router = APIRouter()

@router.get("/badges/{user_id}")
def get_badges(
    user_id: str,
    quiz_id: Optional[str] = Query(None, description="Filter by quiz_id (optional)"),
    scope: Optional[str] = Query(None, description="Filter by scope: 'per_quiz' or 'overall'"),
    session: Session = Depends(get_session)
):
    """
    🎖️ Get all badges for a given user, grouped by scope.
    """
    # Build base query
    query = select(UserBadge).where(UserBadge.user_id == user_id)

    if quiz_id:
        query = query.where(UserBadge.quiz_id == quiz_id)

    if scope:
        query = query.where(UserBadge.scope == scope)

    query = query.order_by(desc(UserBadge.awarded_at))
    user_badges = session.exec(query).all()

    if not user_badges:
        return {
            "user_id": user_id,
            "badge_count": 0,
            "badges": {},
            "message": "No badges found for this user."
        }

    # Group badges by scope
    grouped_badges: Dict[str, List[Dict]] = {"per_quiz": [], "overall": []}

    for badge in user_badges:
        badge_info = {
            "name": badge.badge_name,
            "quiz_id": badge.quiz_id,
            "awarded_at": badge.awarded_at.isoformat()
        }
        grouped_badges.setdefault(badge.scope, []).append(badge_info)

    return {
        "user_id": user_id,
        "badge_count": len(user_badges),
        "badges": grouped_badges
    }
