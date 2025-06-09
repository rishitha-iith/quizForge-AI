from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict
from typing import Annotated
import os
import fitz  # PyMuPDF
from fastapi.openapi.docs import get_redoc_html

# Local modules
from ai_code.question import Question
from ai_code.quiz import Quiz, generate_mcq_questions, parse_questions, shuffle_questions_for_user
from ai_code.userresponse import UserResponse

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

# Load environment variables from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="AI PDF Quiz Generator",
    description="Generate MCQ quizzes from PDFs and manage multi-user quizzes with scoring and leaderboard.",
    version="1.0.0"
)

# Global state
user_quizzes: Dict[str, List[Question]] = {}
user_results: List[Dict] = []
num_users: int = 5  # Default

print("FastAPI App Running")
print(f"OpenAI API Key Loaded: {'Yes' if openai_api_key else 'No'}")

# root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Quiz API!"}

# redocs
@app.get("/redocs", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="API docs")

# ==============================
# 1. Generate Quiz from PDF
# ===============================
@app.post("/generate_quiz", response_model=Quiz, tags=["Quiz Generation"])
async def generate_quiz_endpoint(
    request: Request,
    num_questions: Annotated[int, Form(description="Number of MCQs to generate")],
    num_users_input: Annotated[int, Form(...)],
    pdf_file: UploadFile = File(...)
):
    """
    Upload a PDF file and generate multiple-choice questions.
    """
    print("✅ Route hit!")

    if not pdf_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    if num_questions <= 0:
        raise HTTPException(status_code=422, detail="Number of questions must be greater than zero.")

    if num_users_input <= 0:
        raise HTTPException(status_code=422, detail="Number of users must be greater than zero.")

    try:
        # Read the uploaded PDF
        pdf_content = await pdf_file.read()

        # Extract text
        try:
            with fitz.open(stream=pdf_content, filetype="pdf") as doc:
                text = "".join(page.get_text() for page in doc)
            print("✅ PDF text extracted successfully.")
        except Exception as e:
            print("❌ PDF parsing error:", str(e))
            raise HTTPException(status_code=422, detail="Failed to parse PDF content.")

        # Generate questions using OpenAI
        try:
            print("🧠 Sending to OpenAI...")
            raw_quiz_text = generate_mcq_questions(text, num_questions)
            print("✅ Raw quiz text received:")
            print(raw_quiz_text)
            questions = parse_questions(raw_quiz_text)
        except Exception as e:
            print("❌ OpenAI error:", str(e))
            raise HTTPException(status_code=500, detail="AI failed to generate or format questions.")

        # Set user count globally
        global num_users
        num_users = num_users_input

        return Quiz(
            title=pdf_file.filename.replace(".pdf", "").title() + " Quiz",
            questions=questions
        )

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")



# ===============================
# 2. Start User Quiz
# ===============================
@app.post("/start_user_quiz/{user_id}", tags=["User Quiz Session"])
async def start_user_quiz_endpoint(user_id: str, quiz: Quiz):
    """
    Shuffle and assign quiz questions to a specific user.
    """
    user_quizzes[user_id] = shuffle_questions_for_user(quiz.questions)
    return {"message": f"Quiz started for user {user_id}"}


# ===============================
# 3. Get Quiz for a User
# ===============================
@app.get("/get_user_quiz/{user_id}", response_model=List[Question], tags=["User Quiz Session"])
async def get_user_quiz_endpoint(user_id: str):
    """
    Retrieve the quiz questions assigned to a user.
    """
    if user_id not in user_quizzes:
        raise HTTPException(status_code=404, detail=f"No quiz assigned to user {user_id}")
    return user_quizzes[user_id]


# ===============================
# 4. Submit Answers and Score
# ===============================
@app.post("/submit_user_answers/{user_id}", response_model=UserResponse, tags=["User Responses"])
async def submit_user_answers_endpoint(user_id: str, answers: Dict[int, str]):
    """
    Submit answers for a user's quiz and return the score.
    """
    if user_id not in user_quizzes:
        raise HTTPException(status_code=404, detail=f"No quiz found for user {user_id}")

    quiz = user_quizzes[user_id]
    score = 0

    for i, user_ans in answers.items():
        if 0 <= i < len(quiz):
            correct_letter = chr(65 + quiz[i].correct_index)  # Convert index to A/B/C/D
            if user_ans.upper() == correct_letter:
                score += 1

    time_taken = 0  # Optional: track in future

    # ✅ Overwrite previous result for the same user if it exists
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

    user_response = UserResponse(
        user_id=user_id,
        quiz_id=1,
        answers=answers,
        time_taken=time_taken
    )

    return user_response


# ===============================
# 5. Leaderboard
# ===============================
@app.get("/leaderboard", tags=["Leaderboard"])
async def get_leaderboard():
    """
    Return leaderboard sorted by score and time taken.
    """
    sorted_leaderboard = sorted(user_results, key=lambda x: (-x['score'], x['time_taken']))
    return sorted_leaderboard
