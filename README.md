# 📊 Household Financial Wellness & Debt Dashboard

An **educational, non-advisory financial analytics project** that helps households understand spending behavior, financial health, and debt payoff outcomes using **fully synthetic data**.

This project was developed as part of the **Household Financial Wellness & Debt Optimization Lab** and completed under **CPT-authorized work**.

---

## 🚀 Project Overview

Most households struggle to answer basic financial questions:
- Where is my money going each month?
- How healthy is my financial situation overall?
- How long will it take to become debt-free?
- What happens if my income drops or expenses increase?

This project addresses those questions by combining transaction analytics, financial wellness metrics, debt payoff simulations, and stress-test scenario analysis into a single interactive dashboard designed for non-technical users.

---

## 🧠 Key Features

### 1) Cash-Flow Analytics
- Monthly **income vs expenses** over time
- Net cash-flow trends
- Savings calculations

### 2) Spending Categorization
- Rule-based classification into high-level categories:
  - Housing
  - Food
  - Transport
  - Utilities
  - Healthcare
  - Shopping
  - Entertainment
  - Education
  - Subscriptions
- Visual **expense breakdown** (bar chart)

### 3) Financial Wellness Score (0–100)
A composite score derived from:
- Savings rate
- Spending distribution
- Debt burden indicators

> ⚠️ Educational metric only — not financial advice.

### 4) Debt Payoff Simulation Engine
Supports two common strategies:
- **Debt Snowball** (smallest balance first)
- **Debt Avalanche** (highest interest first)

For each strategy:
- Monthly payment simulation
- Interest accrual
- Payoff timeline
- Total interest paid

### 5) Stress-Test Scenarios
Evaluate how financial shocks affect outcomes:
- **Income drop (–20%)**
- **Expense spike (+30%)**

Each scenario shows:
- Updated savings rate
- Change in wellness score
- New debt payoff timeline
- Increased total interest cost

### 6) Interactive Dashboard (Streamlit)
- Scenario toggle (baseline / income drop / expense spike)
- Strategy toggle (snowball / avalanche)
- Friendly, explainable visuals for non-technical users

---

## 🖥️ Dashboard Preview

The following PDFs demonstrate the Streamlit dashboard under different scenarios:

- [Baseline Scenario](assets/dashboard_pdfs/baseline.pdf)
- [Income Drop Scenario (-20%)](assets/dashboard_pdfs/incomedrop.pdf)
- [Expense Spike Scenario (+30%)](assets/dashboard_pdfs/expense_spike.pdf)

These demonstrate how stress scenarios impact savings and debt payoff outcomes.

--- 

## 🌐 Live Dashboard

👉 [View the live Streamlit dashboard](https://<your-app-url>.streamlit.app)


---

## 🧰 Tech Stack

- **Python**
- **Pandas / NumPy** – data cleaning & analytics
- **Streamlit** – interactive dashboard
- **Rule-based logic** for categorization & simulations
- **CSV-based pipeline** for transparency and reproducibility

No heavy machine learning is used by design — the focus is on explainable analytics.

---

## 📁 Repository Structure

```text
household_finance_lab/
│
├── app.py                     # Streamlit dashboard
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── .gitignore
│
├── data/
│   └── cleaned/               # Synthetic transaction & debt data
│
├── outputs/
│   ├── subtask_d_*.csv        # Debt simulation outputs
│   └── subtask_e_*.csv        # Stress-test & cash-flow outputs
│
├── notebooks/
│   ├── Subtask_B_*.ipynb
│   ├── Subtask_C_*.ipynb
│   ├── Subtask_D_*.ipynb
│   └── Subtask_E_*.ipynb
│
└── assets/
    └── dashboard_pdfs/

---
```

## ▶️ How to Run the Dashboard Locally

### 1) Install dependencies
```bash
pip install -r requirements.txt
```
### 2) Run the Streamlit app
```bash
streamlit run app.py
```
The dashboard will open in your browser at:
```bash
http://localhost:8501
```

🔐 Data Disclaimer
------------------

*   All transaction and debt data used in this project is **fully synthetic**
    
*   No real personal or financial information is included
    
*   This project is **educational only** and **not financial advice**
    

🎓 Academic & Professional Context
----------------------------------

*   Completed as part of **CPT-authorized work**
    
*   Aligned with coursework in:
    
    *   Data Analytics
        
    *   Financial Modeling
        
    *   Simulation & Scenario Analysis
        
*   Designed to demonstrate:
    
    *   End-to-end data pipeline design
        
    *   Analytical reasoning
        
    *   Explainable financial modeling
        
    *   User-focused dashboard development
        

📌 Future Enhancements
----------------------

*   Persona-based dashboards (student, family, single-income, etc.)
    
*   Interactive sliders for custom payment budgets
    
*   Monte Carlo stress simulations
    
*   Deployment on Streamlit Community Cloud
    
*   Integration with synthetic Open Banking APIs
    

👤 Author
---------

**Surya Vardhan Yalavarthi** Graduate Student — Computer Science, University of Cincinnati

GitHub: [https://github.com/suryayalavarthi](https://github.com/suryayalavarthi)
LinkedIn: [https://www.linkedin.com/in/surya-vardhan-yalavarthi/](https://www.linkedin.com/in/surya-vardhan-yalavarthi/)


