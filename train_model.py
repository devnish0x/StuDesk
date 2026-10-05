import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Load cleaned dataset
df = pd.read_csv("data/complaints_dataset_cleaned.csv")

# Input and target
X = df["complaint_text"]
y = df["category"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Model training
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
model.fit(X_train_tfidf, y_train)

# Prediction
y_pred = model.predict(X_test_tfidf)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nClasses:")
print(model.classes_)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=model.classes_))

unique, counts = np.unique(y_pred, return_counts=True)
print("\nPrediction distribution:")
for label, count in zip(unique, counts):
    print(label, "=>", count)

# Save vectorizer and model
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(model, "model.pkl")

print("\nModel and vectorizer saved successfully.")