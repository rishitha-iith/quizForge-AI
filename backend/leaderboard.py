from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session, func
from database import get_session
from models import QuizResult, User, Quiz, Question

router = APIRouter()

# -----------------------------
# 📊 PER-QUIZ LEADERBOARD
# -----------------------------
@router.get("/leaderboard/{quiz_id}")
def get_leaderboard_by_quiz(quiz_id: str, session: Session = Depends(get_session)):
    # 🧠 Check quiz existence
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # 📋 Count total questions for that quiz
    total_marks = session.exec(
        select(func.count()).select_from(Question).where(Question.quiz_id == quiz_id)
    ).first()

    if not total_marks:
        raise HTTPException(status_code=400, detail="No questions found for quiz.")

    # 🏅 Get results with joined user data, ordered by score desc, time asc
    results = session.exec(
        select(User.username, User.user_id, QuizResult.score, QuizResult.time_taken)
        .join(QuizResult, QuizResult.user_id == User.user_id)
        .where(QuizResult.quiz_id == quiz_id)
        .order_by(QuizResult.score.desc(), QuizResult.time_taken.asc())
    ).all()

    leaderboard = [
        {
            "username": username,
            "user_id": user_id,
            "score": score,
            "percentage": round((score / total_marks) * 100, 2),
            "time_taken": time_taken
        }
        for username, user_id, score, time_taken in results
    ]

    return {
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "total_marks": total_marks,
        "leaderboard": leaderboard
    }

# -----------------------------
# 🌐 OVERALL LEADERBOARD
# -----------------------------
@router.get("/overall")
def get_overall_leaderboard(session: Session = Depends(get_session)):
    # 🧾 Fetch all quizzes and their total marks
    quizzes = session.exec(select(Quiz)).all()
    quiz_question_counts = {
        quiz.quiz_id: session.exec(
            select(func.count()).select_from(Question).where(Question.quiz_id == quiz.quiz_id)
        ).first()
        for quiz in quizzes
    }

    # 📊 Fetch all results
    results = session.exec(
        select(QuizResult.user_id, QuizResult.quiz_id, QuizResult.score)
    ).all()

    # 🧮 Aggregate scores
    user_scores = {}
    for user_id, quiz_id, score in results:
        total_marks = quiz_question_counts.get(quiz_id, 0)
        if total_marks == 0:
            continue  # skip malformed data

        if user_id not in user_scores:
            user_scores[user_id] = {'score_sum': 0, 'max_total': 0}

        user_scores[user_id]['score_sum'] += score * 100
        user_scores[user_id]['max_total'] += total_marks * 100

    # 📦 Build leaderboard
    leaderboard = []
    for user_id, score_data in user_scores.items():
        user = session.exec(select(User).where(User.user_id == user_id)).first()
        if not user or score_data['max_total'] == 0:
            continue

        avg_score = round((score_data['score_sum'] / score_data['max_total']) * 100, 2)
        leaderboard.append({
            "username": user.username,
            "user_id": user.user_id,
            "average_score": avg_score
        })

    # 🥇 Sort descending
    leaderboard.sort(key=lambda x: x['average_score'], reverse=True)

    return leaderboard
