## Initial Data Quality Review – Week 1

Dataset: Banking_Transactions_USA_2023_2024.csv

Observations:
- Dataset contains multiple transaction records across 2023–2024.
- Key columns (Transaction_ID, Account_Number, Date, Amount, Merchant) are populated.
- Category field exists but may require standardization.
- No explicit household identifier; account_number will serve as a proxy.
- Transaction amounts require validation for inflow vs outflow interpretation.

Planned Actions:
- Standardize date format
- Normalize transaction amounts
- Remove irrelevant columns for analytics
- Generate cleaned transaction dataset

------------------------------------------------------------------------------------

## Data Quality Report – Transactions (Subtask B)

Dataset: Banking_Transactions_USA_2023_2024.csv

### Raw Dataset Summary
- Total records: 5,389
- Original columns: 20
- Time range: 2023–2024

### Cleaning & Validation Results
- Invalid or unparseable dates: 0
- Missing transaction amounts: 0
- Duplicate transactions detected: 0
- Merchant and category fields normalized to lowercase text

### Schema Standardization
The dataset was standardized to the following fields:
- transaction_id
- account_id
- date
- amount
- merchant
- raw_category

### Assumptions & Notes
- Account_Number is used as a proxy for account_id.
- Household identifiers are not explicitly available in the dataset.
- Transaction amount sign conventions will be standardized in downstream analytics.
- Additional columns were excluded from the cleaned dataset for scope control.

### Output Artifact
- data/cleaned/transactions_clean.csv

------------------------------------------------------------------------------------

## Accounts Data Quality Summary (Subtask B)

- Accounts derived from cleaned transaction data (one record per unique account_id)
- Total accounts: <5389>
- Missing account_id values: 0 (derived from non-null account_id in transactions)
- interest_rate and credit_limit are intentionally null due to source data limitations

Output artifact:
- data/cleaned/accounts_clean.csv

------------------------------------------------------------------------------------

## Debts Data Quality Summary (Subtask B)

- Debt table created as a small synthetic dataset for educational modeling
- Total debt records: 5
- Missing values: 0 across all fields
- Linked to existing account_id values from accounts_clean.csv
- interest_rate stored as APR percentage

Output artifact:
- data/cleaned/debts_clean.csv
