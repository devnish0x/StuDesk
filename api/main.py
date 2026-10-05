from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import csv
from datetime import datetime
from pathlib import Path

from .schemas import ComplaintInput, ComplaintOutput, FeedbackInput
from .routing import department_map

app = FastAPI(
    title="Campus Complaint Intelligence API",
    description="AI-powered complaint classification and routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
LOG_FILE = BASE_DIR / "prediction_logs.csv"
FEEDBACK_FILE = BASE_DIR / "feedback_logs.csv"
MODEL_VERSION = "v1.0"

model = None
vectorizer = None


@app.on_event("startup")
async def load_model():
    global model, vectorizer
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded successfully")


@app.get("/")
async def root():
    return {"message": "Campus Complaint Intelligence API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None, "model_version": MODEL_VERSION}


@app.post("/predict", response_model=ComplaintOutput)
async def predict_complaint(complaint: ComplaintInput):
    text_tfidf = vectorizer.transform([complaint.complaint_text])
    category = model.predict(text_tfidf)[0]
    department = department_map.get(category, "Unknown Department")

    confidence = 1.0

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow([
                "timestamp",
                "complaint_text",
                "predicted_category",
                "department",
                "confidence",
                "model_version"
            ])
        writer.writerow([
            datetime.now().isoformat(),
            complaint.complaint_text,
            category,
            department,
            confidence,
            MODEL_VERSION
        ])

    return ComplaintOutput(
        category=category,
        department=department,
        confidence=confidence
    )


@app.post("/feedback")
async def save_feedback(feedback_data: FeedbackInput):
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow([
                "timestamp",
                "complaint_text",
                "predicted_category",
                "correct_category",
                "feedback",
                "model_version"
            ])
        writer.writerow([
            datetime.now().isoformat(),
            feedback_data.complaint_text,
            feedback_data.predicted_category,
            feedback_data.correct_category,
            feedback_data.feedback,
            MODEL_VERSION
        ])

    return {"message": "Feedback saved successfully"}