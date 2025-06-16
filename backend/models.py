# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid

# ---------- User model ----------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True)
    username: str
    email: str = Field(unique=True)
    password: str  # store hashed password

# ---------- Quiz Result model ----------
class QuizResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # link to User
    quiz_name: str
    score: int
    total: int
    timestamp: str

# ---------- Question model ----------
class QuestionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # Link to the user who received the quiz
    quiz_name: str  # To group questions by quiz
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_index: int  # 0 = A, 1 = B, etc.
    
