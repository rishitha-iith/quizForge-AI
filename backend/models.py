# backend/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid

# Helper for timezone-aware UTC default
def utc_now():
    return datetime.now(timezone.utc)

# -----------------------------
# 🔐 USER MODEL
# -----------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True, unique=True)
    username: str
    email: str = Field(unique=True)
    hashed_password: str

    # Relationships
    quizzes_created: List["Quiz"] = Relationship(back_populates="creator")
    responses: List["UserResponse"] = Relationship(back_populates="user")
    results: List["QuizResult"] = Relationship(back_populates="user")
    badges: List["Badge"] = Relationship(back_populates="user")

# -----------------------------
# 🧪 QUIZ MODEL
# -----------------------------
class Quiz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    quiz_name: str
    max_users: int
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=utc_now)
    difficulty: str = Field(default="medium")
    duration_minutes: Optional[int] = Field(default=None)


    # Relationships
    creator: Optional[User] = Relationship(back_populates="quizzes_created")
    questions: List["Question"] = Relationship(back_populates="quiz")
    participants: List["UserQuiz"] = Relationship(back_populates="quiz")

# -----------------------------
# ❓ QUESTION MODEL
# -----------------------------
class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(default=None, foreign_key="quiz.id")
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_index: int
    explanation: Optional[str] = None
    topic: Optional[str] = None

    quiz: Optional[Quiz] = Relationship(back_populates="questions")

# -----------------------------
# 👥 USER-QUIZ LINK MODEL
# -----------------------------
class UserQuiz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    quiz_id: Optional[int] = Field(default=None, foreign_key="quiz.id")
    started_at: datetime = Field(default_factory=utc_now)

    quiz: Optional[Quiz] = Relationship(back_populates="participants")
    user: Optional[User] = Relationship()

# -----------------------------
# 📥 USER RESPONSE MODEL
# -----------------------------
class UserResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    question_id: Optional[int] = Field(default=None, foreign_key="question.id")
    selected_option: int
    is_correct: bool
    time_taken: int

    user: Optional[User] = Relationship(back_populates="responses")

# -----------------------------
# 🏁 QUIZ RESULT MODEL
# -----------------------------
class QuizResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    quiz_id: Optional[int] = Field(default=None, foreign_key="quiz.id")
    score: int
    accuracy: float
    time_taken: int
    finished_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="results")

# -----------------------------
# 🎖️ BADGE MODEL
# -----------------------------
class Badge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    badge_name: str
    earned_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="badges")

# -----------------------------
# 🔖 Pydantic Schemas
# -----------------------------
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    user_id: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# -----------------------------
# ✅ ANSWER MODEL (User's selected answers)
# -----------------------------
class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    quiz_id: int = Field(foreign_key="quiz.id")
    question_id: int = Field(foreign_key="question.id")
    selected_index: int  # 0, 1, 2, 3
    submitted_at: datetime = Field(default_factory=utc_now)
