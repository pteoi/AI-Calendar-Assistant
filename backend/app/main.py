from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.database import engine, Base
from app.api import agenda, chat

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Calendar Assistant",
    description="An AI-powered calendar assistant to help you manage your schedule and tasks effectively.",
    version="1.0.0",
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agenda.router, prefix="/api/agenda", tags=["Agenda"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat AI"])


@app.get("/")
def root():
    return {"message": "Welcome to the AI Calendar Assistant API!"}
