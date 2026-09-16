import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# File paths
INPUT_PATH = Path("data/cleaned/preprocessed_customer_churn.csv")
OUTPUT_DIR = Path("visualizations")

# Load data
df = pd.read_csv(INPUT_PATH)

print("=== EDA Overview ===")
print("Shape:", df.shape)

print("\n=== Churn Distribution ===")
print(df["churn_flag"].value_counts())

print("\n=== Overall Churn Rate ===")
print(f"{df['churn_flag'].mean():.2%}")


# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 1. Satisfaction Score
# --------------------------------------------------
print("\n=== Churn Rate by Satisfaction Score ===")

satisfaction_churn = (
    df.groupby("satisfaction_score")["churn_flag"]
    .mean()
    .sort_index()
)

print(satisfaction_churn)

satisfaction_churn.plot(
    kind="bar",
    title="Churn Rate by Satisfaction Score"
)

plt.xlabel("Satisfaction Score")
plt.ylabel("Churn Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_satisfaction.png")
plt.close()


# --------------------------------------------------
# 2. Engagement Level
# --------------------------------------------------
print("\n=== Churn Rate by Engagement Level ===")

engagement_churn = (
    df.groupby("engagement_level")["churn_flag"]
    .mean()
    .sort_values(ascending=False)
)

print(engagement_churn)

engagement_churn.plot(
    kind="bar",
    title="Churn Rate by Engagement Level"
)

plt.xlabel("Engagement Level")
plt.ylabel("Churn Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_engagement.png")
plt.close()


# --------------------------------------------------
# 3. Support Tickets
# --------------------------------------------------
print("\n=== Churn Rate by Support Tickets ===")

support_ticket_churn = (
    df.groupby("support_tickets")["churn_flag"]
    .mean()
    .sort_index()
)

print(support_ticket_churn)

support_ticket_churn.plot(
    kind="line",
    marker="o",
    title="Churn Rate by Support Tickets"
)

plt.xlabel("Number of Support Tickets")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_support_tickets.png")
plt.close()


# --------------------------------------------------
# 4. Support Interactions
# --------------------------------------------------
print("\n=== Churn Rate by Support Interactions ===")

support_interaction_churn = (
    df.groupby("support_interactions")["churn_flag"]
    .mean()
    .sort_index()
)

print(support_interaction_churn)

support_interaction_churn.plot(
    kind="line",
    marker="o",
    title="Churn Rate by Support Interactions"
)

plt.xlabel("Number of Support Interactions")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_support_interactions.png")
plt.close()


# --------------------------------------------------
# 5. Returns Count
# --------------------------------------------------
print("\n=== Churn Rate by Returns Count ===")

returns_churn = (
    df.groupby("returns_count")["churn_flag"]
    .mean()
    .sort_index()
)

print(returns_churn)

returns_churn.plot(
    kind="line",
    marker="o",
    title="Churn Rate by Returns Count"
)

plt.xlabel("Number of Returns")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_returns.png")
plt.close()


# --------------------------------------------------
# 6. Days Since Last Purchase
# --------------------------------------------------
print("\n=== Churn Rate by Purchase Recency ===")

# Divide customers into meaningful time ranges
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

recency_churn = (
    df.groupby("purchase_recency_group", observed=False)["churn_flag"]
    .mean()
)

print(recency_churn)

recency_churn.plot(
    kind="bar",
    title="Churn Rate by Days Since Last Purchase"
)

plt.xlabel("Days Since Last Purchase")
plt.ylabel("Churn Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "churn_by_purchase_recency.png")
plt.close()


# --------------------------------------------------
# 7. Customer Segment
# --------------------------------------------------
print("\n=== Churn Rate by Customer Segment ===")

segment_churn = (
    df.groupby("customer_segment")["churn_flag"]
    .mean()
    .sort_values(ascending=False)
)

print(segment_churn)


# --------------------------------------------------
# 8. Customer Value Category
# --------------------------------------------------
print("\n=== Churn Rate by Customer Value Category ===")

value_churn = (
    df.groupby("customer_value_category")["churn_flag"]
    .mean()
    .sort_values(ascending=False)
)

print(value_churn)


print("\n=== EDA Complete ===")
print("Visualizations saved to:", OUTPUT_DIR)