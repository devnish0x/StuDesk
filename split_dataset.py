import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/complaints_dataset_cleaned.csv")

X = df["complaint_text"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nTraining category distribution:")
print(y_train.value_counts())

print("\nTesting category distribution:")
print(y_test.value_counts())