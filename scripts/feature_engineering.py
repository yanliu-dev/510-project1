import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File paths
# --------------------------------------------------
INPUT_PATH = Path("data/cleaned/preprocessed_customer_churn.csv")
OUTPUT_PATH = Path("data/cleaned/customer_churn_final.csv")


# --------------------------------------------------
# Load preprocessed data
# --------------------------------------------------
df = pd.read_csv(INPUT_PATH)

print("=== Preprocessed Dataset ===")
print("Shape:", df.shape)


# --------------------------------------------------
# 1. Create purchase recency groups
# --------------------------------------------------
bins = [0, 30, 60, 90, 180, 270, 365]

labels = [
    "0-30 days",
    "31-60 days",
    "61-90 days",
    "91-180 days",
    "181-270 days",
    "271-365 days"
]

df["purchase_recency_group"] = pd.cut(
    df["days_since_last_purchase"],
    bins=bins,
    labels=labels,
    include_lowest=True
)


# --------------------------------------------------
# 2. Select columns for analysis
# --------------------------------------------------
columns_to_keep = [
    "customer_id",
    "churn_flag",
    "customer_segment",
    "customer_age_months",
    "satisfaction_score",
    "engagement_level",
    "support_tickets",
    "support_interactions",
    "returns_count",
    "days_since_last_purchase",
    "purchase_recency_group",
    "customer_lifetime_value_usd",
    "total_spend_usd",
    "avg_order_value_usd",
    "num_purchases",
    "churn_reason",
    "churn_revenue_impact_usd",
    "customer_country"
]


df_final = df[columns_to_keep].copy()


# --------------------------------------------------
# 3. Check selected data
# --------------------------------------------------
print("\n=== Final Dataset ===")
print("Shape:", df_final.shape)

print("\nColumns:")
print(df_final.columns.tolist())

print("\nMissing values:")
missing_values = df_final.isna().sum()

if missing_values.sum() == 0:
    print("No missing values.")
else:
    print(missing_values[missing_values > 0])


# --------------------------------------------------
# 4. Check churn distribution
# --------------------------------------------------
print("\nChurn flag values:")
print(df_final["churn_flag"].value_counts())


# --------------------------------------------------
# 5. Save final dataset
# --------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df_final.to_csv(OUTPUT_PATH, index=False)

print("\n=== Feature Engineering Complete ===")
print("Final shape:", df_final.shape)
print("Saved to:", OUTPUT_PATH)
