from pydantic import BaseModel
from typing import List
from ai_code.question import Question
from openai import OpenAI
import os
import re
import random
from dotenv import load_dotenv
import json
# Load environment variables from .env file


# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
print("API Key",client.api_key)
class Quiz(BaseModel):
    title: str
    questions: List[Question]

import json

def generate_mcq_questions(text: str, num_questions: int = 5) -> List[Question]:
    prompt = f"""
You are an expert quiz creator.

Generate {num_questions} multiple-choice questions from the following study material.

Output strictly in JSON format:format your answer strictly as valid JSON
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
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://quizforge-ai.onrender.com",
                "X-Title": "QuizForge AI"
            }
        )
        content = response.choices[0].message.content.strip()
        print("=== RAW LLM OUTPUT ===")
        print(content)

        # Parse JSON
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
