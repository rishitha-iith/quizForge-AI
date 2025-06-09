from pydantic import BaseModel
from typing import Dict, List
from ai_code.question import Question
import time

class UserResponse(BaseModel):
    user_id: str
    quiz_id: int
    answers: Dict[int, str]
    time_taken: float = 0

def start_quiz(user_quiz: List[Question], time_limit: int = 600):
    """Run an interactive quiz with user input and timer."""
    score = 0
    start_time = time.time()
    user_answers = {}

    print(f"\n📝 Starting Quiz! You have {time_limit // 60} minutes.\n")

    for i, q in enumerate(user_quiz):
        print(f"\nQ{i+1}: {q.question}")
        for idx, option in enumerate(q.options):
            print(f"{chr(65 + idx)}. {option}")

        valid_input = False
        while not valid_input:
            user_input = input("Enter your answer (A, B, C, D): ").strip().upper()
            if user_input in ["A", "B", "C", "D"]:
                valid_input = True
                user_answers[i] = user_input
            else:
                print("❌ Invalid input. Please enter A, B, C, or D.")

        correct_answer_letter = chr(65 + q.correct_index)
        if user_input == correct_answer_letter:
            score += 1

        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print("\n⏰ Time's up!")
            break

    elapsed_time = time.time() - start_time
    print(f"\n✅ Quiz completed! You scored {score}/{len(user_answers)} in {int(elapsed_time)} seconds.")
    return score, elapsed_time, user_answers
