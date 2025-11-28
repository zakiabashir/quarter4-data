import questionary
import os
from features.transactions.transactions import add_expense, add_income, view_transactions, get_balance
from features.budgets.budgets import set_budget, view_budgets
from features.analytics.analytics import spending_analytics

def main():
    """Main function to run the Personal Finance Tracker CLI."""

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Expense",
                "Add Income",
                "View Transactions",
                "View Balance",
                "Set a budget",
                "View budgets",
                "View spending analytics",
                "Launch Web Dashboard",
                "Exit",
            ],
        ).ask()

        if choice == "Add Expense":
            add_expense()
        elif choice == "Add Income":
            add_income()
        elif choice == "View Transactions":
            view_transactions()
        elif choice == "View Balance":
            get_balance()
        elif choice == "Set a budget":
            set_budget()
        elif choice == "View budgets":
            view_budgets()
        elif choice == "View spending analytics":
            spending_analytics()
        elif choice == "Launch Web Dashboard":
            os.system("streamlit run dashboard.py")
        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()