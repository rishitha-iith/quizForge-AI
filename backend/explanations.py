# backend/explanations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Quiz, Question, User, Answer
import requests, os

router = APIRouter()

@router.get("/explanations/{quiz_name}/{user_id}")
def get_explanations(quiz_name: str, user_id: str, session: Session = Depends(get_session)):
    # Fetch quiz and user
    quiz = session.exec(select(Quiz).where(Quiz.quiz_name == quiz_name)).first()
    user = session.exec(select(User).where(User.user_id == user_id)).first()

    if not quiz or not user:
        raise HTTPException(status_code=404, detail="Quiz or user not found")

    # Fetch questions
    questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()

    # Fetch user's submitted answers
    answers = session.exec(
        select(Answer).where(Answer.user_id == user.id, Answer.quiz_id == quiz.id)
    ).all()
    user_answers = {a.question_id: a.selected_index for a in answers}

    explanation_data = []
    for q in questions:
        correct_index = q.correct_index
        user_index = user_answers.get(q.id, None)
        is_correct = user_index == correct_index

        # Generate explanation
        prompt = (
            f"Explain this MCQ:\n"
            f"Question: {q.question_text}\n"
            f"Options: A: {q.option_a}, B: {q.option_b}, C: {q.option_c}, D: {q.option_d}\n"
            f"Correct answer: {['A','B','C','D'][correct_index]}"
        )

        try:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer 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",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            res.raise_for_status()
            explanation = res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            explanation = f"Error generating explanation: {e}"

        explanation_data.append({
            "question": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "correct_index": correct_index,
            "user_index": user_index,
            "is_correct": is_correct,
            "explanation": explanation
        })

    return {
        "quiz_name": quiz.quiz_name,
        "user_id": user_id,
        "explanations": explanation_data
    }
