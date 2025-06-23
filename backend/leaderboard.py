from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func, Session
from database import get_session
from models import QuizResult, User, Quiz, Question

router = APIRouter()

# -----------------------------
# 📊 PER-QUIZ LEADERBOARD
# -----------------------------
@router.get("/leaderboard/{quiz_id}")
def get_leaderboard_by_quiz(quiz_id: str, session: Session = Depends(get_session)):
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # Get all questions to determine total marks
    questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()
    total_marks = len(questions)

    if total_marks == 0:
        raise HTTPException(status_code=400, detail="No questions found for quiz.")

    results = session.exec(
        select(QuizResult.user_id, QuizResult.score)
        .where(QuizResult.quiz_id == quiz.id)
        .order_by(QuizResult.score.desc())
    ).all()

    leaderboard = []
    for user_id, score in results:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if user:
            leaderboard.append({
                "username": user.username,
                "score": score,
                "percentage": round((score / total_marks) * 100, 2)
            })

    return {
        "quiz_id": quiz_id,
        "quiz_name": quiz.quiz_name,
        "total_marks": total_marks,
        "leaderboard": leaderboard
    }

# -----------------------------
# 🌐 OVERALL LEADERBOARD
# -----------------------------
@router.get("/overall")
def get_overall_leaderboard(session: Session = Depends(get_session)):
    results = session.exec(
        select(QuizResult.user_id, QuizResult.quiz_id, QuizResult.score)
    ).all()

    # Group scores per user
    user_scores = {}
    quiz_totals = {}

    for user_id, quiz_id_fk, score in results:
        quiz = session.exec(select(Quiz).where(Quiz.id == quiz_id_fk)).first()
        if not quiz:
            continue

        total_marks = session.exec(
            select(func.count()).select_from(Question).where(Question.quiz_id == quiz.id)
        ).first()

        if total_marks == 0:
            continue

        if user_id not in user_scores:
            user_scores[user_id] = {'score_sum': 0, 'max_total': 0}

        user_scores[user_id]['score_sum'] += score * 100
        user_scores[user_id]['max_total'] += total_marks * 100

    # Normalize score = sum(score*100)/sum(total*100)
    leaderboard = []
    for user_id, data in user_scores.items():
        user = session.exec(select(User).where(User.id == user_id)).first()
        if user and data['max_total'] > 0:
            avg_score = round((data['score_sum'] / data['max_total']) * 100, 2)
            leaderboard.append({
                "username": user.username,
                "average_score": avg_score
            })

    # Sort descending
    leaderboard.sort(key=lambda x: x['average_score'], reverse=True)

    return leaderboard
