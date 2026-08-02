from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main.agent import agent

# -----------------------------
# Create FastAPI Application
# -----------------------------
app = FastAPI(
    title="DEVFORGE Student Support AI Agent",
    version="1.0.0"
)


# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Home Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to DEVFORGE Student Support AI Agent!",
        "docs": "/docs"
    }


# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    state = {
        "question": request.message,
        "category": "",
        "answer": ""
    }

    result = agent.invoke(state)

    return {
        "question": request.message,
        "category": result["category"],
        "answer": result["answer"]
    }