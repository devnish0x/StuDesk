from pydantic import BaseModel


class ComplaintInput(BaseModel):
    complaint_text: str


class ComplaintOutput(BaseModel):
    category: str
    department: str
    confidence: float


class FeedbackInput(BaseModel):
    complaint_text: str
    predicted_category: str
    correct_category: str
    feedback: str