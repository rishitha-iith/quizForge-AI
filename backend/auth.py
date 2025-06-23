# backend/auth.py

from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi import status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from database import get_session
from models import User
from utils import hash_password, verify_password, create_access_token
from uuid import uuid4
from models import UserCreate, UserRead  # Pydantic schemas

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, session: Session = Depends(get_session)):
    # 1. Check if email already exists
    existing = session.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the incoming plaintext password
    try:
        hashed = hash_password(user_in.password)
    except Exception as exc:
        # If bcrypt is still misconfigured, you'll catch it here
        raise HTTPException(status_code=500, detail="Error hashing password")

    # 3. Create the User object with the hashed password
    new_user = User(
        user_id=str(uuid4()),
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed
    )

    # 4. Persist and return
    session.add(new_user)
    try:
        session.commit()
        session.refresh(new_user)
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error creating user")

    return new_user
@router.post("/login")
def login(identifier: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    # Check for user by email or username
    user = session.exec(
        select(User).where((User.email == identifier) | (User.username == identifier))
    ).first()
    
    # ❗ Fix the password check to use hashed_password
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Create JWT token with user ID
    token = create_access_token({"sub": user.user_id})
    
    return {
        "token": token,
        "user_id": user.user_id,
        "username": user.username
    }
