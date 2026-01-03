from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.habit_tracker import process_log, seed_test_user
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Green Habit Tracker")

class LogPayload(BaseModel):
    user_id: int
    text: str
    timestamp: str = None

@app.on_event("startup")
def startup_event():
    try:
        seed_test_user()
    except Exception:
        pass

@app.post("/api/log")
def log_habit(payload: LogPayload):
    try:
        result = process_log(payload.user_id, payload.text, payload.timestamp)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
