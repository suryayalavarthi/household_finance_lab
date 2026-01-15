import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Financial Wellness & Debt Dashboard", layout="wide")


@st.cache_data
def load_data():
    tx = pd.read_csv("data/cleaned/transactions_clean.csv")
    debts = pd.read_csv("data/cleaned/debts_clean.csv")

    # Subtask D outputs
    d_compare = pd.read_csv("outputs/subtask_d_strategy_comparison.csv")
    d_sched_snow = pd.read_csv("outputs/subtask_d_monthly_schedule_snowball.csv")
    d_sched_ava = pd.read_csv("outputs/subtask_d_monthly_schedule_avalanche.csv")

    # Subtask E outputs
    e_stress = pd.read_csv("outputs/subtask_e_stress_test_summary.csv")
    e_timeline = pd.read_csv("outputs/subtask_e_timeline_impact.csv")

    return tx, debts, d_compare, d_sched_snow, d_sched_ava, e_stress, e_timeline


def to_monthly_cashflow(tx: pd.DataFrame) -> pd.DataFrame:
    tx = tx.copy()
    tx["date"] = pd.to_datetime(tx.get("date"), errors="coerce")
    tx = tx.dropna(subset=["date"])
    tx["month"] = tx["date"].dt.to_period("M").astype(str)

    monthly = (
        tx.groupby("month")
          .agg(
              income=("amount", lambda x: x[x > 0].sum()),
              expenses=("amount", lambda x: abs(x[x < 0].sum()))
          )
          .reset_index()
    )
    monthly["net"] = monthly["income"] - monthly["expenses"]
    return monthly


def ensure_spend_category(tx: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure spend_category exists (recreate using rule-based mapping if missing).
    Keyword rules expanded slightly to reduce "other".
    """
    tx = tx.copy()
    if "spend_category" in tx.columns:
        return tx

    def categorize_spending(merchant, category):
        text = f"{merchant} {category}".lower()

        # Housing
        if any(k in text for k in ["rent", "mortgage", "landlord", "apartment", "lease"]):
            return "housing"

        # Utilities
        if any(k in text for k in ["electric", "water", "gas bill", "utility", "internet", "wifi", "comcast", "verizon", "at&t", "spectrum"]):
            return "utilities"

        # Food
        if any(k in text for k in ["grocery", "kroger", "walmart", "aldi", "costco", "whole foods", "restaurant", "cafe", "coffee", "doordash", "uber eats", "food"]):
            return "food"

        # Transport
        if any(k in text for k in ["gas", "fuel", "shell", "bp", "chevron", "uber", "lyft", "metro", "parking", "toll", "transport"]):
            return "transport"

        # Healthcare
        if any(k in text for k in ["hospital", "clinic", "pharmacy", "cvs", "walgreens", "medical", "dentist", "vision", "health"]):
            return "healthcare"

        # Shopping
        if any(k in text for k in ["amazon", "target", "best buy", "retail", "shopping", "mall", "store"]):
            return "shopping"

        # Entertainment
        if any(k in text for k in ["netflix", "spotify", "hulu", "movie", "cinema", "entertainment", "game", "steam"]):
            return "entertainment"

        # Education
        if any(k in text for k in ["tuition", "university", "college", "course", "udemy", "coursera", "education"]):
            return "education"

        # Subscriptions (separate bucket often helps reduce "other")
        if any(k in text for k in ["subscription", "membership", "prime", "icloud", "google storage"]):
            return "subscriptions"

        return "other"

    if "merchant" not in tx.columns:
        tx["merchant"] = ""
    if "raw_category" not in tx.columns:
        tx["raw_category"] = ""

    tx["spend_category"] = tx.apply(
        lambda r: categorize_spending(str(r["merchant"]), str(r["raw_category"])),
        axis=1
    )
    return tx


def compute_category_breakdown(tx: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    """
    Robust expense/spend distribution by category.
    - Does not assume expenses are negative
    - Shows Top N categories and groups the rest into 'other'
    """
    tx = ensure_spend_category(tx)
    exp = tx.copy()
    exp["abs_amount"] = exp["amount"].abs()

    # Best case: transaction_type exists -> filter to debit-like types
    if "transaction_type" in exp.columns:
        exp = exp[exp["transaction_type"].astype(str).str.lower().isin(["debit", "expense", "withdrawal"])]
    # If most are negative expenses, filter negatives
    elif (exp["amount"] < 0).mean() > 0.5:
        exp = exp[exp["amount"] < 0]
    # Else keep all as spend distribution

    breakdown = (
        exp.groupby("spend_category")["abs_amount"]
           .sum()
           .sort_values(ascending=False)
           .reset_index()
    )

    if breakdown.empty:
        return breakdown

    if len(breakdown) > top_n:
        top = breakdown.head(top_n).copy()
        rest_sum = breakdown["abs_amount"].iloc[top_n:].sum()

        # If "other" already in top, add rest sum into it; else create it
        if "other" in top["spend_category"].values:
            top.loc[top["spend_category"] == "other", "abs_amount"] += rest_sum
        else:
            top = pd.concat([top, pd.DataFrame([{"spend_category": "other", "abs_amount": rest_sum}])], ignore_index=True)

        return top

    return breakdown


# -------------------- UI --------------------

st.title("Household Financial Wellness & Debt Dashboard")
st.caption(
    "Educational, non-advisory dashboard using cleaned transactions and synthetic debt data. "
    "Use Scenario and Strategy controls to explore savings and debt payoff impacts."
)

tx, debts, d_compare, d_sched_snow, d_sched_ava, e_stress, e_timeline = load_data()

# Sidebar controls
st.sidebar.header("Controls")
scenario = st.sidebar.selectbox("Scenario", ["baseline", "income_drop_20pct", "expense_spike_30pct"])
strategy = st.sidebar.radio("Debt Strategy", ["avalanche", "snowball"], horizontal=True)

st.sidebar.markdown("---")
st.sidebar.caption("Switch scenario/strategy to see KPI and payoff differences.")

# Pull scenario row (cashflow KPIs)
stress_row = e_stress[e_stress["scenario"] == scenario].iloc[0]

# KPIs (cashflow + wellness)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Monthly Income", f"{stress_row['monthly_income']:,.2f}")
kpi2.metric("Monthly Expenses", f"{stress_row['monthly_expenses']:,.2f}")
kpi3.metric("Monthly Savings", f"{stress_row['monthly_savings']:,.2f}")
kpi4.metric("Savings Rate", f"{stress_row['savings_rate_percent']:.2f}%")

if "wellness_score" in e_stress.columns:
    kpi5.metric("Wellness Score", f"{stress_row['wellness_score']:.2f}/100")
else:
    kpi5.metric("Wellness Score", "N/A")

# Row 1: Cashflow over time + Category breakdown
monthly_cf = to_monthly_cashflow(tx)
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Income vs Expenses Over Time")
    st.caption("Tracks monthly income, expenses, and net cashflow (income minus expenses).")
    if len(monthly_cf) == 0:
        st.warning("No valid dates found to build monthly cashflow.")
    else:
        st.line_chart(monthly_cf.set_index("month")[["income", "expenses", "net"]], use_container_width=True)

with c2:
    st.subheader("Expense Breakdown by Category")
    st.caption("Shows where spending is concentrated across high-level categories.")
    cat = compute_category_breakdown(tx, top_n=8)
    if cat.empty:
        st.warning("No category data available to chart.")
    else:
        st.bar_chart(cat.set_index("spend_category")["abs_amount"], use_container_width=True)

# Row 2: Debts table + Strategy comparison
c3, c4 = st.columns([1, 2])

with c3:
    st.subheader("Current Debts")
    st.caption("Balances, APR, and minimum payments for the sample household debts.")
    st.dataframe(
        debts[["debt_id", "current_balance", "interest_rate", "minimum_payment"]],
        use_container_width=True
    )

with c4:
    st.subheader("Snowball vs Avalanche (Baseline Comparison)")
    st.caption("Compares payoff duration and total interest paid under each strategy.")
    st.dataframe(d_compare, use_container_width=True)

# Row 3: Payoff timeline (baseline schedules from Subtask D)
st.subheader("Debt Payoff Timeline (Total Balance)")
st.caption("Shows remaining total debt balance over months under the selected strategy (baseline).")

sched = d_sched_ava.copy() if strategy == "avalanche" else d_sched_snow.copy()
timeline = sched[["month", "total_balance", "total_interest_paid_to_date"]].copy().set_index("month")
st.line_chart(timeline[["total_balance"]], use_container_width=True)

# Row 4: Stress scenario impact on payoff (clear KPIs + clean table)
st.subheader("Stress Scenario Impact (Avalanche)")
st.caption("Shows how stress scenarios change the payoff timeline and total interest under the Avalanche strategy.")

impact_cols = ["scenario", "monthly_budget", "months_to_payoff", "total_interest_paid"]
missing_cols = [c for c in impact_cols if c not in e_timeline.columns]

if missing_cols:
    st.warning(
        f"Timeline impact file is missing columns: {missing_cols}. "
        "Please re-save outputs/subtask_e_timeline_impact.csv with these fields."
    )
    st.dataframe(e_timeline, use_container_width=True)
else:
    impact_row = e_timeline[e_timeline["scenario"] == scenario].iloc[0]

    s1, s2, s3 = st.columns(3)
    s1.metric("Scenario Monthly Debt Budget", f"{impact_row['monthly_budget']:,.2f}")
    s2.metric("Months to Payoff (Scenario)", int(impact_row["months_to_payoff"]))
    s3.metric("Total Interest Paid (Scenario)", f"{impact_row['total_interest_paid']:,.2f}")

    st.dataframe(e_timeline[impact_cols], use_container_width=True)
