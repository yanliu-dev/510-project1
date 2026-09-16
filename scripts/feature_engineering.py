import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File paths
# --------------------------------------------------
INPUT_PATH = Path("data/cleaned/preprocessed_customer_churn.csv")
OUTPUT_PATH = Path("data/cleaned/customer_churn_final.csv")


# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(INPUT_PATH)

print("=== Feature Engineering ===")
print("Original shape:", df.shape)


# --------------------------------------------------
# 1. Create Purchase Recency Group
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
# 2. Select final variables
# --------------------------------------------------
columns_to_keep = [
    "customer_id",
    "churn_flag",

    # Customer profile
    "customer_segment",
    "customer_age_months",

    # Main churn-related factors
    "satisfaction_score",
    "engagement_level",
    "support_tickets",
    "support_interactions",
    "returns_count",
    "days_since_last_purchase",
    "purchase_recency_group",

    # Customer value
    "customer_lifetime_value_usd",
    "total_spend_usd",
    "avg_order_value_usd",
    "num_purchases",

    # Churn / business impact
    "churn_reason",
    "churn_revenue_impact_usd"
]


df_final = df[columns_to_keep].copy()


# --------------------------------------------------
# 3. Remove incomplete customer record
# --------------------------------------------------
# Remove rows where the main analytical features are missing.
df_final = df_final.dropna(
    subset=[
        "customer_age_months",
        "satisfaction_score",
        "engagement_level",
        "support_tickets",
        "support_interactions",
        "returns_count",
        "days_since_last_purchase"
    ]
)


# --------------------------------------------------
# 4. Check final dataset
# --------------------------------------------------
print("\n=== Final Dataset ===")
print("Shape:", df_final.shape)

print("\nColumns:")
print(df_final.columns.tolist())

print("\nMissing Values:")
print(df_final.isna().sum())

print("\nChurn Distribution:")
print(df_final["churn_flag"].value_counts())


# --------------------------------------------------
# 5. Save final dataset
# --------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df_final.to_csv(OUTPUT_PATH, index=False)

print("\n=== Feature Engineering Complete ===")
print("Final dataset saved to:", OUTPUT_PATH)

