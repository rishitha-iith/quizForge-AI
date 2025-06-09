from pydantic import BaseModel
from typing import List
from ai_code.question import Question
from openai import OpenAI
import os
import re
import random
from dotenv import load_dotenv

# Load environment variables from .env file
# This is necessary for the OpenAI API key to be available
# in the environment
load_dotenv()
print("Basic main.py running")
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=openai_api_key)
print(f"API Key: {openai_api_key}")

class Quiz(BaseModel):
    title: str
    questions: List[Question]

def generate_mcq_questions(text: str, num_questions: int = 5) -> str:
    prompt = f"""
You are an expert quiz creator.

Generate {num_questions} multiple-choice questions (with 4 options: A, B, C, D) from the following study material.
Each question must include:
1. A question
2. Four options (A–D)
3. The correct answer (e.g., Correct Answer: B)

Study Material:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_questions(raw_text: str) -> List[Question]:
    """Parse raw quiz text into structured Question objects."""
    blocks = raw_text.strip().split("\n\n")
    questions = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 6:
            continue  # Skip if format is broken

        question_text = lines[0]
        options = lines[1:5]

        match = re.search(r"Correct Answer: ([A-D])", lines[5])
        if not match:
            continue

        correct_letter = match.group(1)
        correct_index = "ABCD".index(correct_letter)

        questions.append(Question(question=question_text, options=options, correct_index=correct_index))

    return questions

def shuffle_questions_for_user(questions: List[Question]) -> List[Question]:
    """Shuffle question order and option order for a user's quiz."""
    q_copy = [q.model_copy() for q in questions]
    random.shuffle(q_copy)

    for q in q_copy:
        opts = q.options.copy()
        correct_answer = opts[q.correct_index]
        random.shuffle(opts)
        q.options = opts
        q.correct_index = opts.index(correct_answer)

    return q_copy