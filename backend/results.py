from fastapi import APIRouter, Form, Depends, HTTPException
from sqlmodel import select, Session
from typing import Dict
from models import Question, Quiz, QuizResult, User, UserQuiz, UserBadge, Answer
from database import get_session
from datetime import datetime
import json

router = APIRouter()

@router.post("/submit_answers")
def submit_answers(
    user_id: str = Form(...),
    answers: str = Form(...),
    quiz_id: str = Form(...),
    session: Session = Depends(get_session)
):
    # 👤 Validate User
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # 🧾 Validate Quiz
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # ⛔ Prevent Resubmission
    existing_result = session.exec(
        select(QuizResult).where(
            (QuizResult.user_id == user_id) & 
            (QuizResult.quiz_id == quiz_id)
        )
    ).first()
    if existing_result:
        raise HTTPException(status_code=403, detail="You have already submitted this quiz.")

    # ⏱ Fetch Quiz Start Info
    user_quiz = session.exec(
        select(UserQuiz).where(
            (UserQuiz.user_id == user_id) & 
            (UserQuiz.quiz_id == quiz_id)
        )
    ).first()
    if not user_quiz:
        raise HTTPException(status_code=400, detail="Quiz was not started properly.")

    started_at = user_quiz.started_at
    finished_at = datetime.now()
    time_taken = int((finished_at - started_at).total_seconds() // 60)

    # 🧾 Parse Answer JSON
    try:
        if isinstance(answers, str):
            answer_map = json.loads(answers)
            if isinstance(answer_map, str):
                answer_map = json.loads(answer_map)
        else:
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid answers format.")

    # 🧠 Fetch Quiz Questions
    questions = session.exec(select(Question).where(Question.quiz_id == quiz_id)).all()

    # 🧮 Score Calculation
    score = 0
    for q in questions:
        qid_str = str(q.id)
        if qid_str in answer_map:
            user_ans = answer_map[qid_str].upper()
            correct_ans = ["A", "B", "C", "D"][q.correct_index]
            if user_ans == correct_ans:
                score += 1
                
    total_questions = len(questions)
    accuracy = (score / total_questions) * 100 if total_questions > 0 else 0.0
    # ✅ Save Individual Answers
    # ✅ Save Individual Answers
    for q in questions:
        qid_str = str(q.id)
        if qid_str in answer_map:
            user_ans = answer_map[qid_str].upper()
            selected_index = {"A": 0, "B": 1, "C": 2, "D": 3}.get(user_ans)
            if selected_index is None:
                continue  # 🚨 Skip invalid answers
        else:
            continue  # 🚨 Skip unanswered questions

        # ✅ Only add if selected_index is valid
        answer = Answer(
            user_id=user_id,
            quiz_id=quiz_id,
            question_id=q.id,
            selected_index=selected_index,
            submitted_at=finished_at
        )
        session.add(answer)

        session.commit()
        # 💾 Save Quiz Result
        result = QuizResult(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            accuracy=accuracy,
            time_taken=time_taken,
            finished_at=finished_at
        )
        session.add(result)
        session.commit()

        # 🏅 Badge Assignment
        badge_name = (
            "Perfect Scorer" if accuracy == 100 else
            "Quiz Master" if accuracy >= 80 else
            "Good Attempt" if accuracy >= 50 else
            "Participant"
        )
        scope = "per_quiz"

        existing_badge = session.exec(
            select(UserBadge).where(
                (UserBadge.user_id == user_id) &
                (UserBadge.quiz_id == quiz_id) &
                (UserBadge.badge_name == badge_name) &
                (UserBadge.scope == scope)
            )
        ).first()

        if not existing_badge:
            new_badge = UserBadge(
                user_id=user_id,
                quiz_id=quiz_id,
                badge_name=badge_name,
                scope=scope
            )
            session.add(new_badge)
        session.commit()

    return {
        "status": "submitted",
        "user_id": user_id,
        "quiz_id": quiz_id,
        "quiz_name": quiz.quiz_name,
        "score": score,
        "total": total_questions,
        "accuracy": accuracy,
        "time_taken": time_taken,
        "badge_awarded": badge_name
    }
