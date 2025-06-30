from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Quiz, Question, User, Answer
import requests

router = APIRouter()

# 🔐 OpenRouter config
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b:free"

# Helper to convert index to letter
def index_to_letter(index):
    return ["A", "B", "C", "D"][index] if index is not None and 0 <= index <= 3 else None

@router.get("/explanations/{quiz_id}/{user_id}")
def get_explanations(quiz_id: str, user_id: str, session: Session = Depends(get_session)):
    # 🎯 Validate quiz and user
    quiz = session.exec(select(Quiz).where(Quiz.quiz_id == quiz_id)).first()
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not quiz or not user:
        raise HTTPException(status_code=404, detail="Quiz or user not found")

    # ❓ Fetch questions
    questions = session.exec(select(Question).where(Question.quiz_id == quiz.quiz_id)).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this quiz")

    # ✅ Fetch user's answers
    answers = session.exec(
        select(Answer).where(
            Answer.quiz_id == quiz_id,
            Answer.user_id == user_id
        )
    ).all()
    user_answers = {ans.question_id: ans.selected_index for ans in answers}

    # 📘 Generate explanations
    explanation_data = []
    for q in questions:
        correct_index = q.correct_index
        user_index = user_answers.get(q.id)
        is_correct = user_index == correct_index

        prompt = (
            f"Explain why the correct answer is {index_to_letter(correct_index)} for this MCQ:\n\n"
            f"Question: {q.question_text}\n"
            f"Options:\n"
            f"A. {q.option_a}\n"
            f"B. {q.option_b}\n"
            f"C. {q.option_c}\n"
            f"D. {q.option_d}\n"
        )

        try:
            res = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            res.raise_for_status()
            explanation = res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            explanation = f"Explanation not available due to error: {e}"

        explanation_data.append({
            "question": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "correct_index": correct_index,
            "correct_option": index_to_letter(correct_index),
            "user_index": user_index,
            "user_option": index_to_letter(user_index),
            "is_correct": is_correct,
            "explanation": explanation
        })

    return {
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "user_id": user.user_id,
        "explanations": explanation_data
    }
