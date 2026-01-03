## Core Data Schema – Initial Version

### Transactions
Source: Banking_Transactions_USA_2023_2024.csv

| Field | Type | Source Column |
|----|----|----|
| transaction_id | string | Transaction_ID |
| account_id | string | Account_Number |
| date | datetime | Transaction_Date |
| amount | float | Transaction_Amount |
| merchant | string | Merchant_Name |
| raw_category | string | Category |

Notes:
- Transaction_ID is unique per record.
- Account_Number will be used as account_id.
- Transaction_Amount values appear positive for both inflows and outflows and will be standardized later.

------------------------------------------------------------------------------------

## Transactions Table (Final – Subtask B)

| Field | Type | Description |
|------|-----|------------|
| transaction_id | string | Unique transaction identifier |
| account_id | string | Bank account identifier |
| date | datetime | Transaction date |
| amount | float | Transaction amount |
| merchant | string | Merchant or counterparty |
| raw_category | string | Original transaction category |

Primary Key:
- transaction_id

Notes:
- Cleaned dataset stored as transactions_clean.csv
- Schema designed for downstream categorization and metric computation

------------------------------------------------------------------------------------

## Accounts Table (Subtask B)

| Field | Type | Description |
|------|------|------------|
| account_id | string | Unique account identifier (from transactions) |
| account_type | string | Account type (default: checking) |
| interest_rate | float | Interest rate (nullable; not available in source) |
| credit_limit | float | Credit limit (nullable; not available in source) |

Notes:
- Accounts table was derived by deduplicating account_id values in cleaned transactions.
- Interest rate and credit limit fields are intentionally left null for future extension.
- Output artifact: data/cleaned/accounts_clean.csv
