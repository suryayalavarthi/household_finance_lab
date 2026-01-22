# Subtask A – Define Personas, Accounts & Data Audit
**Project:** Household Financial Wellness & Debt Optimization Lab  
**Purpose:** Define sample household personas, the accounts they use, and audit available dataset fields for pipeline compatibility.

---

## 1) Household Personas (3–5)

### Persona 1: Student (Part-time job + tight budget)
**Profile**
- Lives with roommates or campus housing
- Income from part-time job / assistantship
- High sensitivity to rent, food, and transport costs

**Typical Accounts**
- Checking account (primary transactions)
- Savings account (small emergency fund)
- 1 credit card (low/moderate limit)
- Student loan (optional)

**Primary Financial Goals**
- Avoid overdraft / late fees
- Build emergency savings
- Reduce revolving credit card balance

---

### Persona 2: Young Professional (Single income)
**Profile**
- Full-time job, early career
- Moderate discretionary spending (shopping, subscriptions)
- May carry credit card debt

**Typical Accounts**
- Checking account (salary + spending)
- Savings account (emergency fund)
- 1–2 credit cards
- Auto loan (optional)

**Primary Financial Goals**
- Improve savings rate
- Reduce high APR debt
- Stabilize fixed vs variable spending

---

### Persona 3: Young Couple (Dual income, building stability)
**Profile**
- Two incomes
- Shared rent/mortgage and bills
- May have multiple debts (credit cards + personal loan)

**Typical Accounts**
- Joint checking account (bills)
- Individual checking/savings (optional)
- 2–4 credit cards
- Personal loan / auto loan (optional)

**Primary Financial Goals**
- Build savings buffer
- Reduce total interest paid on debt
- Plan for medium-term goals (car/house)

---

### Persona 4: Family with Kids (High fixed costs)
**Profile**
- Higher fixed expenses (rent/mortgage, childcare, groceries)
- Lower flexibility in variable spend
- Multiple recurring bills

**Typical Accounts**
- Checking account
- Savings account
- 2+ credit cards
- Mortgage / auto loan
- Medical expense account (optional)

**Primary Financial Goals**
- Protect monthly surplus
- Maintain stability under shocks (medical bills, income change)
- Reduce debt burden safely

---

### Persona 5: Single Parent / Single Income Household (High risk sensitivity)
**Profile**
- Single income, high responsibilities
- More vulnerable to income drops and expense spikes

**Typical Accounts**
- Checking account
- Savings account (emergency fund priority)
- 1–2 credit cards
- Auto loan / personal loan (optional)

**Primary Financial Goals**
- Maintain minimum savings buffer
- Reduce high-interest debt
- Increase resilience to shocks

---

## 2) Account Types (Scope)
This project supports the following generic account types:
- **Checking** (income deposits, bill payments, daily spending)
- **Savings** (emergency fund / goal-based savings)
- **Credit Cards** (revolving debt with APR and minimum payment)
- **Installment Loans** (personal loan / auto loan with APR and minimum payment)
- **Mortgage** (optional extension; treated as installment debt in future work)

---

## 3) Data Audit – Available Dataset Fields

### Data Sources Used
- Synthetic transaction dataset (CSV)
- Synthetic debt dataset (CSV)
- Project outputs (Subtasks C–F) stored as CSV for reproducibility

### Transaction Dataset – Expected Fields (Schema Target)
| Field | Description | Required |
|---|---|---|
| date | transaction date | Yes |
| account | account identifier (or proxy) | Preferred |
| amount | signed amount (income vs expense) | Yes |
| merchant | merchant/payee name | Preferred |
| raw_category | raw or source category | Preferred |
| spend_category | mapped high-level category | Derived |
| needs_vs_wants | needs vs wants label | Derived |
| fixed_or_variable | fixed vs variable label | Derived |

### Debt Dataset – Expected Fields (Schema Target)
| Field | Description | Required |
|---|---|---|
| debt_id | unique identifier | Yes |
| current_balance | current outstanding balance | Yes |
| interest_rate | APR (decimal or percent) | Yes |
| minimum_payment | minimum monthly payment | Yes |
| debt_type | credit card / loan | Preferred |

### Notes on Data Quality / Compatibility
- Date should parse to a standard datetime format.
- Amount should be numeric. If sign conventions vary, the pipeline uses robust absolute spend logic for category breakdown.
- Missing values are handled via basic cleaning rules (drop/standardize where appropriate).
- Data is synthetic and used for educational modeling only.

---

## 4) Field Coverage Summary

After loading the synthetic datasets, the following fields were confirmed.

### Transactions CSV – Observed Columns
- `transaction_id`
- `account_id`
- `date`
- `amount`
- `merchant`
- `raw_category`

**Derived fields used downstream (Subtasks C–F):**
- `spend_category`
- `needs_vs_wants`
- `fixed_or_variable`
- `month` (derived from date)

---

### Debts CSV – Observed Columns
- `debt_id`
- `account_id`
- `current_balance`
- `interest_rate`
- `minimum_payment`

**Assumptions:**
- Each debt record represents one revolving or installment account.
- Interest rate is expressed as APR and converted internally for monthly simulations.
- Minimum payment is treated as a fixed monthly obligation unless overridden by payoff strategy logic.

---

## 5) Submission Notes
- Personas are designed for storytelling and scenario-based evaluation.
- Data audit ensures the pipeline’s schemas can support Subtasks B–F consistently.
- All datasets used are synthetic and the project is educational/non-advisory.
