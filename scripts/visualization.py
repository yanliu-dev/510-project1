"""Generate six customer churn visualizations and save them to outputs.

Dataset:
https://www.kaggle.com/datasets/datascikhan/e-commerce-customer-churn-2026/data

"""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


FILE_NAME = "customer_churn_final.csv"
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / FILE_NAME
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


def save_figure(fig, output_dir, filename):
    """Save one figure and close it."""
    output_path = output_dir / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_grouped_churn(
    data,
    group_column,
    order,
    colors,
    title,
    xlabel,
    output_dir,
    filename,
):
    """Create and save one grouped churn-rate bar chart."""
    churn_rate = (
        data.groupby(group_column, observed=False)["churn_flag"]
        .mean()
        .reindex(order)
    )
    overall_churn_rate = data["churn_flag"].mean()

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(churn_rate.index, churn_rate.values, color=colors)

    ax.bar_label(
        bars,
        labels=[f"{value:.1%}" for value in churn_rate.values],
        padding=3,
    )

    ax.axhline(
        y=overall_churn_rate,
        color="gray",
        linestyle="--",
        label="Overall Churn Rate",
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Churn Rate")
    ax.legend()

    return save_figure(fig, output_dir, filename)


def create_risk_signals(data):
    """Create five binary signals and their total count."""
    data["low_satisfaction_signal"] = (
        data["satisfaction_score"] <= 2
    ).astype(int)

    data["low_engagement_signal"] = (
        data["engagement_level"] == "Low"
    ).astype(int)

    data["high_support_signal"] = (
        data["support_tickets"] >= 12
    ).astype(int)

    data["high_returns_signal"] = (
        data["returns_count"] >= 5
    ).astype(int)

    data["purchase_inactivity_signal"] = (
        data["days_since_last_purchase"] >= 61
    ).astype(int)

    risk_signal_columns = [
        "low_satisfaction_signal",
        "low_engagement_signal",
        "high_support_signal",
        "high_returns_signal",
        "purchase_inactivity_signal",
    ]

    data["risk_signal_count"] = data[risk_signal_columns].sum(axis=1)


def create_investment_level(data):
    """Create the relationship investment score and five levels."""
    investment_features = [
        "total_spend_usd",
        "num_purchases",
        "customer_age_months",
    ]

    percentile_cols = []

    for column in investment_features:
        percentile_column = column + "_percentile"
        data[percentile_column] = data[column].rank(pct=True) * 100
        percentile_cols.append(percentile_column)

    data["relationship_investment_score"] = (
        data[percentile_cols].mean(axis=1)
    )

    investment_order = [
        "Very Low",
        "Low",
        "Medium",
        "High",
        "Very High",
    ]

    data["investment_level"] = pd.qcut(
        data["relationship_investment_score"],
        q=5,
        labels=investment_order,
    )

    return investment_order


def plot_heatmap(data, investment_order, output_dir):
    """Create and save the combined churn-rate heatmap."""
    heatmap_data = data.pivot_table(
        index="risk_signal_count",
        columns="investment_level",
        values="churn_flag",
        aggfunc="mean",
        observed=False,
    )

    heatmap_data = heatmap_data.reindex(
        index=range(6),
        columns=investment_order,
    )

    heatmap_data = heatmap_data * 100

    investment_overall = (
        data.groupby("investment_level", observed=False)["churn_flag"]
        .mean()
        .reindex(investment_order)
        * 100
    )

    signal_overall = (
        data.groupby("risk_signal_count")["churn_flag"]
        .mean()
        .reindex(range(6))
        * 100
    )

    x_labels = [
        f"{level}\nOverall: {investment_overall[level]:.1f}%"
        for level in investment_order
    ]

    y_labels = [
        f"{number} {'signal' if number == 1 else 'signals'}\n"
        f"Overall: {signal_overall[number]:.1f}%"
        for number in range(6)
    ]

    heatmap_labels = heatmap_data.round(1).astype(str) + "%"

    fig, ax = plt.subplots(figsize=(11, 7))

    sns.heatmap(
        heatmap_data,
        annot=heatmap_labels,
        fmt="",
        cmap="Blues",
        vmin=0,
        vmax=100,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Churn Rate (%)"},
        ax=ax,
    )

    ax.collections[0].colorbar.ax.invert_yaxis()

    ax.set_xticklabels(
        x_labels,
        rotation=0,
    )

    ax.set_yticklabels(
        y_labels,
        rotation=0,
    )

    label_color = "#1F4E79"

    ax.set_title(
        "Customer Churn Rate Varies More by Risk Signals Than Past Investment",
        fontsize=14,
        fontweight="bold",
        color=label_color,
    )

    ax.set_xlabel(
        "Past Investment",
        fontsize=12,
        fontweight="bold",
        color=label_color,
        labelpad=10,
    )

    ax.set_ylabel(
        "Number of Risk Signals",
        fontsize=12,
        fontweight="bold",
        color=label_color,
        labelpad=10,
    )

    return save_figure(
        fig,
        output_dir,
        "06_risk_signals_and_past_investment.png",
    )


def generate_visualizations(data_path, output_dir):
    """Load the dataset, generate six figures, and return their paths."""
    data = pd.read_csv(data_path)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    saved_files = []

    # ---------------------------------------------------
    # 1. Satisfaction score & churn rate
    # ---------------------------------------------------

    satisfaction_order = [5, 4, 3, 2, 1]

    satisfaction_labels = [
        "Very Satisfied",
        "Satisfied",
        "Neutral",
        "Dissatisfied",
        "Very Dissatisfied",
    ]

    satisfaction_churn_rate = (
        data.groupby("satisfaction_score")["churn_flag"]
        .mean()
        .reindex(satisfaction_order)
    )

    overall_churn_rate = data["churn_flag"].mean()

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        satisfaction_labels,
        satisfaction_churn_rate.values,
        color=[
            "lightgray",
            "lightgray",
            "lightgray",
            "blue",
            "blue",
        ],
    )

    ax.bar_label(
        bars,
        labels=[
            f"{value:.1%}"
            for value in satisfaction_churn_rate.values
        ],
        padding=3,
    )

    ax.axhline(
        y=overall_churn_rate,
        color="gray",
        linestyle="--",
        label="Overall Churn Rate",
    )

    ax.set_title(
        "Customer Churn Rate by Satisfaction Score"
    )

    ax.set_xlabel(
        "Satisfaction Level"
    )

    ax.set_ylabel(
        "Churn Rate"
    )

    ax.legend()

    saved_files.append(
        save_figure(
            fig,
            output_dir,
            "01_churn_by_satisfaction.png",
        )
    )

    # ---------------------------------------------------
    # 2. Engagement level & churn rate
    # ---------------------------------------------------

    engagement_order = [
        "High",
        "Medium",
        "Low",
    ]

    saved_files.append(
        plot_grouped_churn(
            data=data,
            group_column="engagement_level",
            order=engagement_order,
            colors=[
                "lightgray",
                "lightgray",
                "blue",
            ],
            title="Customer Churn Rate by Engagement Levels",
            xlabel="Engagement Levels",
            output_dir=output_dir,
            filename="02_churn_by_engagement.png",
        )
    )

    # ---------------------------------------------------
    # 3. Support tickets & churn rate
    # ---------------------------------------------------

    data["support_ticket_group"] = pd.cut(
        data["support_tickets"],
        bins=[
            -1,
            3,
            7,
            11,
            15,
            19,
        ],
        labels=[
            "0-3",
            "4-7",
            "8-11",
            "12-15",
            "16-19",
        ],
    )

    tickets_order = [
        "0-3",
        "4-7",
        "8-11",
        "12-15",
        "16-19",
    ]

    saved_files.append(
        plot_grouped_churn(
            data=data,
            group_column="support_ticket_group",
            order=tickets_order,
            colors=[
                "lightgray",
                "lightgray",
                "lightgray",
                "blue",
                "blue",
            ],
            title="Customer Churn Rate by Number of Support Tickets",
            xlabel="Number of Support Tickets Raised",
            output_dir=output_dir,
            filename="03_churn_by_support_tickets.png",
        )
    )

    # ---------------------------------------------------
    # 4. Returns & churn rate
    # ---------------------------------------------------

    data["return_group"] = pd.cut(
        data["returns_count"],
        bins=[
            -1,
            2,
            4,
            6,
            8,
            9,
        ],
        labels=[
            "0-2",
            "3-4",
            "5-6",
            "7-8",
            "9",
        ],
    )

    returns_order = [
        "0-2",
        "3-4",
        "5-6",
        "7-8",
        "9",
    ]

    saved_files.append(
        plot_grouped_churn(
            data=data,
            group_column="return_group",
            order=returns_order,
            colors=[
                "gray",
                "gray",
                "blue",
                "blue",
                "blue",
            ],
            title="Customer Churn Rate by Number of Returns",
            xlabel="Number of Returns",
            output_dir=output_dir,
            filename="04_churn_by_returns.png",
        )
    )

    # ---------------------------------------------------
    # 5. Days since last purchase & churn rate
    # ---------------------------------------------------

    data["days_purchase_group"] = pd.cut(
        data["days_since_last_purchase"],
        bins=[
            0,
            30,
            60,
            90,
            180,
            364,
        ],
        labels=[
            "1-30",
            "31-60",
            "61-90",
            "91-180",
            "181-364",
        ],
    )

    days_order = [
        "1-30",
        "31-60",
        "61-90",
        "91-180",
        "181-364",
    ]

    saved_files.append(
        plot_grouped_churn(
            data=data,
            group_column="days_purchase_group",
            order=days_order,
            colors=[
                "lightgray",
                "lightgray",
                "blue",
                "blue",
                "blue",
            ],
            title="Churn Rate by Days Since Last Purchase",
            xlabel="Days Since Last Purchase",
            output_dir=output_dir,
            filename="05_churn_by_days_since_last_purchase.png",
        )
    )

    # ---------------------------------------------------
    # 6. Risk signals + past investment
    # ---------------------------------------------------

    create_risk_signals(data)

    investment_order = create_investment_level(data)

    saved_files.append(
        plot_heatmap(
            data,
            investment_order,
            output_dir,
        )
    )

    return saved_files


def parse_args():
    """Read optional data and output paths from the command line."""
    parser = ArgumentParser(
        description="Generate six customer churn figures."
    )

    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to the raw churn CSV.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for the six PNG figures.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    generated_files = generate_visualizations(
        args.data_path,
        args.output_dir,
    )

    print("Generated figures:")

    for generated_file in generated_files:
        print(generated_file)