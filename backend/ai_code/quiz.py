import requests
import json
import re
import random
from typing import List
from pydantic import BaseModel
from ai_code.question import Question

# Define your OpenRouter API key directly (not secure for production!)
OPENROUTER_API_KEY = "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"

class Quiz(BaseModel):
    title: str
    questions: List[Question]

def generate_mcq_questions(text: str, num_questions: int = 5) -> List[Question]:
    prompt = f"""
You are an expert quiz creator.

Generate {num_questions} multiple-choice questions from the following study material.

Output strictly in JSON format: format your answer strictly as valid JSON
{{
  "questions": [
    {{
      "type": "multiple-choice",
      "difficulty": "easy",
      "question": "Your question here",
      "correctAnswer": "A",
      "choices": [
        "A) ...",
        "B) ...",
        "C) ...",
        "D) ..."
      ]
    }}
  ]
}}

Study Material:
{text[:3000]}
"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer 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",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://quizforge-ai.onrender.com",  # Optional for usage tracking
                "X-Title": "QuizForge AI"  # Optional for model usage attribution
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        if response.status_code != 200:
            raise ValueError(f"OpenRouter API error: {response.status_code} - {response.text}")

        content = response.json()["choices"][0]["message"]["content"].strip()
        print("=== RAW LLM OUTPUT ===")
        print(content)

        # Clean JSON if it's wrapped in backticks
        match = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)
        if match:
            content = match.group(1).strip()

        response_json = json.loads(content)
        return parse_questions(response_json["questions"])

    except Exception as e:
        print("Error during question generation:", str(e))
        raise ValueError("LLM error or bad JSON response.") from e


def parse_questions(json_questions: List[dict]) -> List[Question]:
    questions = []
    for q in json_questions:
        question_text = q["question"]
        options = q["choices"]
        correct_letter = q["correctAnswer"]

        # Convert "A" → index 0, "B" → 1, etc.
        correct_index = "ABCD".index(correct_letter.upper())
        questions.append(Question(question=question_text, options=options, correct_index=correct_index))

    return questions


def shuffle_questions_for_user(questions: List[Question]) -> List[Question]:
    """
    Shuffle questions and their options for a user session.
    """
    q_copy = [q.model_copy() for q in questions]
    random.shuffle(q_copy)

    for q in q_copy:
        original_options = q.options.copy()
        correct_answer = original_options[q.correct_index]
        random.shuffle(original_options)
        q.options = original_options
        q.correct_index = original_options.index(correct_answer)

    return q_copy
