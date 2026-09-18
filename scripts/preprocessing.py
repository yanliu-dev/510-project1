import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File paths
# --------------------------------------------------
INPUT_PATH = Path("data/raw/E-commerce_Customer_Churn_2026.csv")
OUTPUT_PATH = Path("data/cleaned/preprocessed_customer_churn.csv")


# --------------------------------------------------
# Load raw data
# --------------------------------------------------
df = pd.read_csv(INPUT_PATH)

print("=== Raw Dataset Overview ===")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# --------------------------------------------------
# 1. Check missing values
# --------------------------------------------------
print("\n=== Missing Values Before Cleaning ===")

missing_values = df.isna().sum()

if missing_values.sum() == 0:
    print("No missing values found.")
else:
    print(missing_values[missing_values > 0])


# --------------------------------------------------
# 2. Check duplicate rows
# --------------------------------------------------
print("\n=== Duplicate Rows Before Cleaning ===")

duplicate_count = df.duplicated().sum()
print(duplicate_count)


# --------------------------------------------------
# 3. Remove duplicate rows
# --------------------------------------------------
df = df.drop_duplicates()

print("\nAfter removing duplicates:")
print("Shape:", df.shape)


# --------------------------------------------------
# 4. Clean churn_flag
# --------------------------------------------------
df["churn_flag"] = pd.to_numeric(
    df["churn_flag"],
    errors="coerce"
)

# Remove rows where churn_flag cannot be converted
df = df.dropna(subset=["churn_flag"])

# Convert churn_flag to integer
df["churn_flag"] = df["churn_flag"].astype(int)


# --------------------------------------------------
# 5. Final data quality checks
# --------------------------------------------------
print("\n=== Final Data Quality Check ===")

print("Final shape:", df.shape)

print("\nMissing values:")
remaining_missing = df.isna().sum()

if remaining_missing.sum() == 0:
    print("No missing values.")
else:
    print(remaining_missing[remaining_missing > 0])

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nChurn flag values:")
print(df["churn_flag"].value_counts())


# --------------------------------------------------
# 6. Save cleaned data
# --------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print("\n=== Preprocessing Complete ===")
print("Cleaned shape:", df.shape)
print("Saved to:", OUTPUT_PATH)