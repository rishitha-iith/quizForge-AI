from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.openapi.docs import get_redoc_html
from pydantic import BaseModel
from typing import List, Dict, Annotated
from dotenv import load_dotenv
from openai import OpenAI
import os
import fitz  # PyMuPDf
import json
import re

# Local modules
from ai_code.question import Question
from ai_code.quiz import Quiz, parse_questions, shuffle_questions_for_user
from ai_code.userresponse import UserResponse

# Load environment variables

# Initialize FastAPI app
app = FastAPI(
    title="AI PDF Quiz Generator",
    description="Generate MCQ quizzes from PDFs and manage multi-user quizzes with scoring and leaderboard.",
    version="1.0.0"
)

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
print("API Key",client.api_key)

# Global state
user_quizzes: Dict[str, List[Question]] = {}
user_results: List[Dict] = []
num_users: int = 5  # default



@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Quiz API!"}


@app.get("/redocs", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="API docs")


# ========================================
# 1. Generate Quiz from PDF
# ========================================
@app.post("/generate_quiz", response_model=Quiz, tags=["Quiz Generation"])
async def generate_quiz_endpoint(
    request: Request,
    num_questions: Annotated[int, Form(description="Number of MCQs to generate")],
    num_users_input: Annotated[int, Form(...)],
    pdf_file: UploadFile = File(...)
):
    """
    Upload a PDF and generate MCQs using OpenRouter DeepSeek model.
    """
    if not pdf_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    if num_questions <= 0:
        raise HTTPException(status_code=422, detail="Number of questions must be greater than zero.")
    if num_users_input <= 0:
        raise HTTPException(status_code=422, detail="Number of users must be greater than zero.")

    try:
        pdf_content = await pdf_file.read()
        print(f"Received PDF file: {pdf_file.filename} ({len(pdf_content)} bytes)")

        # Extract text
        try:
            with fitz.open(stream=pdf_content, filetype="pdf") as doc:
                text = "".join(page.get_text() for page in doc)
        except Exception as e:
            raise HTTPException(status_code=422, detail="Failed to parse PDF content.") from e

        # Create prompt
        prompt = (
            f"Generate {num_questions} multiple-choice questions from the following text.\n"
            f"Each question should have 4 options and a correct_option (0-based index).\n"
            f"Return the result in JSON list format like:\n"
            f"Return only raw JSON (no markdown, no explanation). Do NOT wrap it in ```json``` or any backticks."
            f"[{{'question': '...', 'options': ['A', 'B', 'C', 'D'], 'correct_option': 2}}, ...]\n\n"
            f"Text:\n{text[:3000]}"
        )

        # Call OpenRouter LLM
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "https://quizforge-ai.onrender.com",
                    "X-Title": "QuizForge AI"
                }
            )
            raw_output = response.choices[0].message.content.strip()

            # Remove triple backticks and optional `json` label
            match = re.search(r"```(?:json)?\s*(.*?)```", raw_output, re.DOTALL)
            if match:
                raw_output = match.group(1).strip()

            print("=== CLEANED OUTPUT ===")
            print(raw_output)

            # Try to parse
            parsed = json.loads(raw_output)
            questions = [Question(question=q['question'], options=q['options'], correct_index=q['correct_option']) for q in parsed]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM error or bad JSON: {str(e)}")

        # Update user count
        global num_users
        num_users = num_users_input
        print("PDF Text Preview:\n", text[:1000])
        # Return quiz
        return Quiz(
            title=pdf_file.filename.replace(".pdf", "").title() + " Quiz",
            questions=questions
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# ========================================
# 2. Start User Quiz
# ========================================
@app.post("/start_user_quiz/{user_id}", tags=["User Quiz Session"])
async def start_user_quiz_endpoint(user_id: str, quiz: Quiz):
    """
    Shuffle and assign quiz questions to a user.
    """
    user_quizzes[user_id] = shuffle_questions_for_user(quiz.questions)
    return {"message": f"Quiz started for user {user_id}"}


# ========================================
# 3. Get Quiz for a User
# ========================================
@app.get("/get_user_quiz/{user_id}", response_model=List[Question], tags=["User Quiz Session"])
async def get_user_quiz_endpoint(user_id: str):
    """
    Get quiz questions assigned to a user.
    """
    if user_id not in user_quizzes:
        raise HTTPException(status_code=404, detail=f"No quiz found for user {user_id}")
    return user_quizzes[user_id]


# ========================================
# 4. Submit Answers and Score
# ========================================
@app.post("/submit_user_answers/{user_id}", response_model=UserResponse, tags=["User Responses"])
async def submit_user_answers_endpoint(user_id: str, answers: Dict[int, str]):
    """
    Submit answers and receive score and metadata.
    """
    if user_id not in user_quizzes:
        raise HTTPException(status_code=404, detail=f"No quiz found for user {user_id}")

    quiz = user_quizzes[user_id]
    score = 0

    for i, user_ans in answers.items():
        if 0 <= i < len(quiz):
            correct_letter = chr(65 + quiz[i].correct_index)
            if user_ans.upper() == correct_letter:
                score += 1

    time_taken = 0  # You can add logic to track this in future

    # Save/overwrite result
    existing = next((r for r in user_results if r["user_id"] == user_id), None)
    if existing:
        existing["score"] = score
        existing["time_taken"] = time_taken
    else:
        user_results.append({
            "user_id": user_id,
            "score": score,
            "time_taken": time_taken
        })

    return UserResponse(
        user_id=user_id,
        quiz_id=1,
        answers=answers,
        time_taken=time_taken
    )


# ========================================
# 5. Leaderboard
# ========================================
@app.get("/leaderboard", tags=["Leaderboard"])
async def get_leaderboard():
    """
    Return leaderboard sorted by score and time taken.
    """
    sorted_leaderboard = sorted(user_results, key=lambda x: (-x['score'], x['time_taken']))
    return sorted_leaderboard
