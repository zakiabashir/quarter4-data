import streamlit as st
from datetime import datetime
import pandas as pd

from features.transactions.database import read_transactions
from features.budgets.database import read_budgets

def main():
    st.set_page_config(layout="centered", page_title="Finance Dashboard")

    st.title("Finance Dashboard")

    # Load data
    transactions = read_transactions()
    budgets = read_budgets()

    # --- Balance Section ---
    st.header("Current Balance")
    
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    total_income = 0
    total_expenses = 0

    for t in transactions:
        if t['date'].startswith(current_month):
            if t['type'] == 'Income':
                total_income += t['amount']
            else:
                total_expenses += t['amount']
    
    balance = total_income - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rs {total_income / 100:.2f}", delta_color="normal")
    col2.metric("Total Expenses", f"Rs {total_expenses / 100:.2f}", delta_color="inverse")
    col3.metric("Balance", f"Rs {balance / 100:.2f}", delta=f"{balance - (total_income - total_expenses):.2f}")


    # --- Budget Status Section ---
    st.header("Budget Status")

    spent_by_category = {}
    for t in transactions:
        if t['type'] == 'Expense' and t['date'].startswith(current_month):
            category = t['category']
            spent_by_category[category] = spent_by_category.get(category, 0) + t['amount']

    for category, budget in budgets.items():
        spent = spent_by_category.get(category, 0)
        remaining = budget - spent
        utilization = (spent / budget) * 100 if budget > 0 else 0
        
        st.subheader(category)
        col1, col2, col3 = st.columns(3)
        col1.metric("Budget", f"Rs {budget / 100:.2f}")
        col2.metric("Spent", f"Rs {spent / 100:.2f}")
        col3.metric("Remaining", f"Rs {remaining / 100:.2f}")
        
        st.progress(min(100, int(utilization)))


    # --- Recent Transactions Table ---
    st.header("Recent Transactions")

    if transactions:
        df = pd.DataFrame(transactions)
        df['amount'] = df['amount'] / 100
        df = df.sort_values(by="date", ascending=False).head(10)
        
        st.dataframe(df.style.apply(
            lambda x: ['color: green' if x.type == 'Income' else 'color: red' for i in x],
            axis=1
        ))

if __name__ == "__main__":
    main()
