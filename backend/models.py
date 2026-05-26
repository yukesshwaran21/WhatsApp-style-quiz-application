from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(str(v)):
            raise ValueError("Invalid ObjectId")
        return str(v)

# ─── Quiz Session Models ───────────────────────────────────────────
class StartSessionRequest(BaseModel):
    user_id: str
    exam_id: str
    subject_id: str
    chapter_id: str

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_option: int
    question_shown_at: datetime
    answer_submitted_at: datetime

class FinishSessionRequest(BaseModel):
    session_id: str
