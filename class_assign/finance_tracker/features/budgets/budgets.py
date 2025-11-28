import questionary
from rich.console import Console
from rich.table import Table
from rich.progress_bar import ProgressBar
from datetime import datetime
from features.budgets.database import add_budget as db_add_budget, read_budgets
from features.transactions.database import read_transactions

def set_budget():
    """Sets a budget for a specific category."""

    category = questionary.select(
        "Select category to set a budget for:",
        choices=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"],
    ).ask()

    amount_str = questionary.text(f"Enter the budget for {category}:").ask()
    try:
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    db_add_budget(category, amount)
    print(f"Budget for {category} set to {amount / 100:.2f}")


def view_budgets():
    """Displays all budgets in a table with spending and remaining amounts."""
    budgets = read_budgets()
    transactions = read_transactions()
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    spent_by_category = {}
    for t in transactions:
        if t['type'] == 'Expense' and t['date'].startswith(current_month):
            category = t['category']
            spent_by_category[category] = spent_by_category.get(category, 0) + t['amount']

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category")
    table.add_column("Budget")
    table.add_column("Spent")
    table.add_column("Remaining")
    table.add_column("Utilization", width=20)
    table.add_column("Status")

    for category, budget in budgets.items():
        spent = spent_by_category.get(category, 0)
        remaining = budget - spent
        utilization = (spent / budget) * 100 if budget > 0 else 0

        status = "[green]OK[/green]"
        if utilization > 100:
            status = "[red]Over[/red]"
        elif utilization > 70:
            status = "[yellow]Warning[/yellow]"

        budget_display = f"{budget / 100:.2f}"
        spent_display = f"{spent / 100:.2f}"
        remaining_display = f"{remaining / 100:.2f}"
        
        utilization_bar = ProgressBar(total=100)
        utilization_bar.update(min(100, utilization))


        table.add_row(
            category,
            budget_display,
            spent_display,
            remaining_display,
            utilization_bar,
            status,
        )

    console.print(table)
