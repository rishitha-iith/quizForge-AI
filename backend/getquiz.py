from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Quiz, Question, UserQuiz, User, QuizResult

router = APIRouter()

@router.get("/get_quiz/{quiz_id}/{user_id}")
def get_quiz_by_id(quiz_id: str, user_id: str, session: Session = Depends(get_session)):
    # 🔍 Fetch the quiz
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 🔍 Fetch the user
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ⛔ Prevent reattempts
    existing_result = session.exec(
        select(QuizResult).where(
            (QuizResult.quiz_id == quiz.quiz_id) & (QuizResult.user_id == user.user_id)
        )
    ).first()
    if existing_result:
        raise HTTPException(status_code=403, detail="You have already attempted this quiz.")

    # 🚫 Max participants check
    participant_count = session.exec(
        select(UserQuiz).where(UserQuiz.quiz_id == quiz.quiz_id)
    ).all()
    if len(participant_count) >= quiz.max_users:
        raise HTTPException(status_code=403, detail="Max participants limit reached.")

    # ✅ Register user as participant if not already
    existing_participant = session.exec(
        select(UserQuiz).where(
            (UserQuiz.quiz_id == quiz.quiz_id) & (UserQuiz.user_id == user.user_id)
        )
    ).first()
    if not existing_participant:
        session.add(UserQuiz(user_id=user.user_id, quiz_id=quiz.quiz_id))
        quiz.participants_attempted += 1
        session.add(quiz)
        session.commit()

    # 📋 Fetch all questions for this quiz
    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz.quiz_id)
    ).all()

    # 🧾 Format question data with indexed IDs
    question_data = [
        {
            "question_id": idx,  # Manual indexing
            "question": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d]
        }
        for idx, q in enumerate(questions)
    ]

    return {
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "difficulty": quiz.difficulty,
        "duration_minutes": quiz.duration_minutes,
        "max_users": quiz.max_users,
        "participants_attempted": quiz.participants_attempted,
        "questions": question_data
    }
