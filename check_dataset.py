import pandas as pd

df = pd.read_csv("data/complaints_dataset.csv")

# Strip spaces from all string columns
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].str.strip()

print("First 5 rows of dataset:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nUnique categories:")
print(df["category"].unique())

print("\nCategory counts:")
print(df["category"].value_counts())

print("\nUnique priorities:")
print(df["priority"].unique())

print("\nUnique departments:")
print(df["department"].unique())

print("\nDuplicate rows:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv("data/complaints_dataset_cleaned.csv", index=False)
print("\nCleaned dataset saved as data/complaints_dataset_cleaned.csv")