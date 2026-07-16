# server.py

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.exceptions import AgentError
from config import Config
from main import build_controller  # reuse your existing wiring, unchanged

app = FastAPI(title="AI Coding Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config.load()
Path(config.workspace).mkdir(parents=True, exist_ok=True)
controller = build_controller(config)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/api/health")
def health():
    return {"status": "ok", "model": config.model}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        answer = controller.run(req.message)
    except AgentError as error:
        return ChatResponse(answer=f"agent error: {error}")
    return ChatResponse(answer=answer)


# Serve the frontend (static/index.html) at "/"
app.mount("/", StaticFiles(directory="static", html=True), name="static")