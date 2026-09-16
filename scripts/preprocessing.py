import pandas as pd
from pathlib import Path


# File paths
INPUT_PATH = Path("data/raw/E-commerce_Customer_Churn_2026.csv")
OUTPUT_PATH = Path("data/cleaned/preprocessed_customer_churn.csv")


# Load raw data
df = pd.read_csv(INPUT_PATH)

print("=== Dataset Overview ===")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n=== Missing Values ===")
print(df.isna().sum())

print("\n=== Duplicate Rows ===")
print(df.duplicated().sum())

print("\n=== Data Types ===")
print(df.dtypes)

print("\n=== Churn Flag Values ===")
print(df["churn_flag"].value_counts(dropna=False))


# Basic cleaning
df = df.drop_duplicates()

# Remove rows with missing target values
df = df.dropna(subset=["churn_flag"])


# Save preprocessed data
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("\n=== Preprocessing Complete ===")
print("Cleaned shape:", df.shape)
print("Saved to:", OUTPUT_PATH)