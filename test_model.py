import joblib

# Load saved model and vectorizer
vectorizer = joblib.load("vectorizer.pkl")
model = joblib.load("model.pkl")

# Sample complaint texts
sample_complaints = [
    "The hostel bathroom water supply is not coming regularly",
    "The bus is arriving late every day",
    "My attendance was marked absent incorrectly",
    "The canteen food smells bad and is not hygienic",
    "The classroom projector is not working",
    "My scholarship approval is still pending",
    "The lab computers cannot connect to the internet"
]

# Convert text to TF-IDF
sample_tfidf = vectorizer.transform(sample_complaints)

# Predict categories
predictions = model.predict(sample_tfidf)

# Category to department mapping
department_map = {
    "Hostel": "Hostel Office",
    "Transport": "Transport Office",
    "Academics": "Academic Section",
    "Canteen": "Canteen Management",
    "Facilities": "Maintenance Department",
    "Administration": "Admin Office",
    "IT Support": "IT Helpdesk"
}

# Show results
for complaint, category in zip(sample_complaints, predictions):
    department = department_map.get(category, "Unknown Department")
    print("\nComplaint:", complaint)
    print("Predicted Category:", category)
    print("Routed Department:", department)