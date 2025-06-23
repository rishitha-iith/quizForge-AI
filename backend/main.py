# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import create_db_and_tables
from auth import router as auth_router
from ai_code.quiz import router as quiz_router
from results import router as results_router
from leaderboard import router as leaderboard_router
from badges import router as badges_router
from explanations import router as explanations_router
from getquiz import router as get_quiz_router 

# Lifespan context to run code on startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up... creating database tables.")
    create_db_and_tables()
    yield
    print("🛑 Shutting down... cleanup if needed.")

# Main app instance with lifespan handler
app = FastAPI(
    title="QuizForge AI",
    lifespan=lifespan
)

# CORS middleware (Allow all origins for now - restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use: ["http://localhost:3000"] or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health-check route
@app.get("/")
def read_root():
    return {"message": "Welcome to QuizForge AI Backend!"}

# Registering all routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])
app.include_router(get_quiz_router, tags=["Quiz"])
app.include_router(results_router, prefix="/results", tags=["Results"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["Leaderboard"])
app.include_router(badges_router, prefix="/badges", tags=["Badges"])
app.include_router(explanations_router, prefix="/explanations", tags=["Explanations"])
