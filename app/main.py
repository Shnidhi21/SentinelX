from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path

# Add the app directory to Python's module search path
APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from detection.incident_analyzer import analyze_incident


app = FastAPI(
    title="SentinelX",
    description="AI-powered cybersecurity threat detection and response platform",
    version="1.0.0"
)


class SecurityEvent(BaseModel):
    event_type: str
    source_ip: Optional[str] = "unknown"
    username: Optional[str] = "unknown"


class IncidentRequest(BaseModel):
    events: List[SecurityEvent]
    ai_result: str
    severity_score: int


@app.get("/")
def root():

    return {
        "name": "SentinelX",
        "status": "online",
        "description": "AI-powered cybersecurity threat detection and response platform"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(request: IncidentRequest):

    events = [
        event.model_dump()
        for event in request.events
    ]

    result = analyze_incident(
        events=events,
        ai_result=request.ai_result,
        severity_score=request.severity_score
    )

    return result