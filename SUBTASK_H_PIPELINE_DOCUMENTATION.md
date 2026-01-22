# Subtask H – Documentation, Ethics & Future Extensions (Master Pipeline Doc)
**Project:** Household Financial Wellness & Debt Optimization Lab  
**Artifact Type:** End-to-end pipeline documentation + ethics + future volunteer playbook  
**Data Note:** All datasets used in this repository are **synthetic** and the project is **educational / non-advisory**.

---

## 1) Pipeline Overview (End-to-End)

This project implements a simplified personal finance analytics pipeline:

1. **Ingest cleaned transaction + debt datasets** (CSV)
2. **Map transactions into high-level categories** (rule-based)
3. **Label needs vs wants** + **fixed vs variable**
4. **Compute household financial metrics** (savings rate, breakdowns)
5. **Compute a Financial Wellness Score (0–100)** (explainable scoring)
6. **Simulate debt payoff timelines** under Snowball vs Avalanche
7. **Stress test scenarios** (income drop / expense spike) and evaluate impacts
8. **Serve insights via Streamlit dashboard** for non-technical users

Primary outputs are stored as CSV files for reproducibility and transparency.

---

## 2) Data Model (Core Schema)

### 2.1 Transactions (Observed Columns)
From `data/cleaned/transactions_clean.csv`:

| Field | Type | Description |
|---|---|---|
| transaction_id | string/int | Unique transaction identifier |
| account_id | string/int | Account identifier associated with transaction |
| date | date | Transaction date |
| amount | float | Signed transaction amount (income vs expense) |
| merchant | string | Merchant / payee name |
| raw_category | string | Raw category from source |

**Derived fields created in Subtask C and used in downstream tasks:**
- `month` (derived from date)
- `spend_category` (high-level category mapping)
- `needs_vs_wants` (rule-based label)
- `fixed_or_variable` (rule-based label)

---

### 2.2 Debts (Observed Columns)
From `data/cleaned/debts_clean.csv`:

| Field | Type | Description |
|---|---|---|
| debt_id | string/int | Unique debt identifier |
| account_id | string/int | Account identifier |
| current_balance | float | Current outstanding balance |
| interest_rate | float | APR (annual percentage rate) |
| minimum_payment | float | Minimum monthly payment |

---

## 3) Categorization Logic (Rule-Based)

### 3.1 High-level Spend Categories
Transactions are mapped into high-level categories such as:
- housing, food, transport, utilities, healthcare, shopping, entertainment, education, subscriptions, other

Mapping uses keyword rules over `merchant` + `raw_category`. Example rule patterns:
- If merchant/category contains “rent”, “mortgage” → `housing`
- If contains “kroger”, “grocery”, “restaurant” → `food`
- If contains “uber”, “lyft”, “fuel”, “parking” → `transport`

**Design choice:** Rule-based logic is used to keep the system explainable and easy to modify.

---

### 3.2 Needs vs Wants
Rule-based separation:
- **Needs**: housing, utilities, groceries/basic food, healthcare, transport (commuting)
- **Wants**: entertainment, discretionary shopping, non-essential subscriptions

This is intentionally approximate and used for educational analytics.

---

### 3.3 Fixed vs Variable
Rule-based separation:
- **Fixed**: rent/mortgage, utilities, insurance, loan payments, recurring subscriptions
- **Variable**: groceries, dining out, shopping, entertainment, travel

---

## 4) Financial Metrics (Subtask C)

Computed monthly/household-level metrics include:

- **Savings rate**
  - `savings_rate = (income - expenses) / income * 100`
- **Expense breakdown**
  - category totals, needs vs wants totals
- **Fixed vs variable split**
  - monthly fixed cost vs variable spend

These metrics provide the foundation for wellness scoring and scenario analysis.

---

## 5) Financial Wellness Score (0–100)

### 5.1 Score Philosophy
The score is explainable and intended to reflect:
- savings behavior
- spending stability
- debt burden pressure

### 5.2 Example Explainable Score Components (Template)
A simple scoring approach can be structured as:

- **Savings rate component (0–50 points)**
  - Higher savings rate → higher points
- **Spending balance component (0–25 points)**
  - Lower concentration in discretionary categories → higher points
- **Debt burden component (0–25 points)**
  - Lower debt-to-income pressure → higher points

**Note:** The exact weights/rules can be adjusted by future volunteers.

---

## 6) Debt Payoff Simulation (Subtask D)

### 6.1 Strategies
Two payoff strategies are implemented:

- **Debt Snowball**
  - Focus extra payment on **smallest balance** first
- **Debt Avalanche**
  - Focus extra payment on **highest interest rate** first

### 6.2 Simulation Assumptions
- Simulation runs monthly.
- APR is converted to a monthly rate: `monthly_rate = apr / 12`.
- Interest accrues on remaining balance each month.
- Monthly payment budget is allocated:
  1) at least minimum payments
  2) remaining budget goes to target debt (snowball/avalanche priority)
- Simulation ends when all balances reach ~0.


### 6.3 Output Tables

The debt payoff simulation produces structured CSV outputs to support
analysis, stress testing, and dashboard visualization.

**Monthly payoff schedules**
- `subtask_d_monthly_schedule_snowball.csv`
- `subtask_d_monthly_schedule_avalanche.csv`

Each file contains month-by-month balances, interest accrual, and cumulative interest paid.

**Payoff duration summaries**
- `subtask_d_payoff_months_snowball.csv`
- `subtask_d_payoff_months_avalanche.csv`

These files summarize total months required to eliminate all debts under each strategy.

**Strategy comparison**
- `subtask_d_strategy_comparison.csv`

Provides a side-by-side comparison of Snowball vs Avalanche strategies
(months to payoff and total interest paid).

**Stress testing outputs (Subtask E)**
- `subtask_e_stress_test_summary.csv`
- `subtask_e_timeline_impact.csv`

These files capture scenario-based impacts (income drop, expense spike)
on savings, wellness metrics, and debt payoff timelines.



---

## 7) Stress Testing (Subtask E)

### 7.1 Scenarios
Two scenarios are evaluated:

- **Income drop (–20%)**
- **Expense spike (+30%)**

### 7.2 Stress Outputs
For each scenario:
- recalculated savings rate and monthly savings
- updated wellness score (if included)
- payoff timeline impact (months to payoff, total interest) using adjusted monthly debt budget

---

## 8) Dashboard Layout (Subtask F)

The Streamlit dashboard is designed for non-technical users and includes:

- KPI cards:
  - monthly income, expenses, savings, savings rate, wellness score
- income vs expenses line chart
- category breakdown bar chart
- current debts table
- snowball vs avalanche baseline comparison
- debt payoff timeline chart
- stress scenario impact KPIs (months to payoff + total interest)
- stress scenario impact summary table

---

## 9) Ethics, Disclaimers, and Responsible Use

### 9.1 Educational / Non-Advisory Disclaimer
- This project is for **education and demonstration only**.
- It does **not** provide financial, legal, or tax advice.
- Outputs are based on simplified assumptions and synthetic data.

### 9.2 Data Privacy
- All data in this repository is **synthetic**.
- No personally identifying information (PII) is used.

### 9.3 Bias / Limitations
- Rule-based categorization can misclassify merchants.
- Needs vs wants assumptions vary by household context.
- Wellness score is a simplified metric and not a standardized industry score.

### 9.4 Safe Communication Style
Recommendations are phrased as:
- “Consider…”, “May help…”, “In general…”
and avoid prescriptive advice.

---

## 10) Future Volunteer Playbook

### 10.1 Plug in a New Dataset
To use a new dataset, ensure the following minimum columns:

**Transactions**
- date, amount, merchant, raw_category (plus optional account_id)

**Debts**
- current_balance, interest_rate, minimum_payment (plus optional account_id)

Place files in:
- `data/cleaned/transactions_clean.csv`
- `data/cleaned/debts_clean.csv`

Then run:
- Subtask C notebook to generate derived labels and metrics
- Subtask D notebook to generate payoff schedules
- Subtask E notebook for stress scenario outputs
- `streamlit run app.py` to view dashboard

---

### 10.2 Change Scoring Rules
- Update the wellness score calculation in the Subtask C/E notebook.
- Keep changes explainable:
  - document new weights
  - provide example calculation for one scenario
- Re-save `outputs/subtask_e_stress_test_summary.csv` with updated `wellness_score`.

---

### 10.3 Add More Sophisticated ML (Optional)
Possible extensions:
- **Clustering spender types** (k-means) using category proportions
- **Forecasting monthly income/expenses** (moving average, regression)
- **Anomaly detection** for unusual spending spikes

Guidelines:
- Keep baseline rules as fallback (explainable)
- Validate on synthetic data first
- Document model assumptions and limitations

---

## 11) Run Instructions (Repository)
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Start dashboard:
```bash
streamlit run app.py
```

## 12) Submission Notes
--------------------

This document describes the complete pipeline used across Subtasks A–G and supports Subtask H requirements:

*   core schemas for transactions and debts
    
*   categorization + metric logic
    
*   wellness score explanation
    
*   debt simulation assumptions
    
*   dashboard layout
    
*   ethics & disclaimers
    
*   future volunteer playbook for extension

---
