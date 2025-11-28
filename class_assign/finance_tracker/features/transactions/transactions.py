
import questionary
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from features.transactions.database import add_transaction as db_add_transaction, read_transactions

def add_expense():
    """Adds a new expense transaction."""
    amount_str = questionary.text("Enter the amount:").ask()
    try:
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = questionary.select(
        "Select expense category:",
        choices=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"],
    ).ask()

    description = questionary.text("Enter a description:").ask()

    date_str = questionary.text(
        "Enter the date (YYYY-MM-DD), or leave empty for today:",
        default=datetime.now().strftime("%Y-%m-%d")
    ).ask()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    transaction = {
        "date": date.strftime("%Y-%m-%d"),
        "type": "Expense",
        "category": category,
        "amount": amount,
        "description": description,
    }
    db_add_transaction(transaction)
    print("Expense added successfully!")

def add_income():
    """Adds a new income transaction."""
    amount_str = questionary.text("Enter the amount:").ask()
    try:
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = questionary.select(
        "Select income source:",
        choices=["Salary", "Freelance", "Business", "Investment", "Gift", "Other"],
    ).ask()

    description = questionary.text("Enter a description:").ask()

    date_str = questionary.text(
        "Enter the date (YYYY-MM-DD), or leave empty for today:",
        default=datetime.now().strftime("%Y-%m-%d")
    ).ask()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    transaction = {
        "date": date.strftime("%Y-%m-%d"),
        "type": "Income",
        "category": category,
        "amount": amount,
        "description": description,
    }
    db_add_transaction(transaction)
    print("Income added successfully!")

def view_transactions():
    """Displays all transactions in a table with optional filtering."""
    transactions = read_transactions()

    if not transactions:
        print("No transactions found.")
        return

    filter_choice = questionary.select(
        "Filter transactions:",
        choices=["All", "Last 7 days", "Expenses only", "Income only"],
    ).ask()

    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    filtered_transactions = []
    for t in transactions:
        transaction_date = datetime.strptime(t['date'], "%Y-%m-%d")
        if filter_choice == "All":
            filtered_transactions.append(t)
        elif filter_choice == "Last 7 days" and transaction_date >= seven_days_ago:
            filtered_transactions.append(t)
        elif filter_choice == "Expenses only" and t['type'] == 'Expense':
            filtered_transactions.append(t)
        elif filter_choice == "Income only" and t['type'] == 'Income':
            filtered_transactions.append(t)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Amount", justify="right")

    for transaction in sorted(filtered_transactions, key=lambda t: t['date'], reverse=True):
        color = "green" if transaction["type"] == "Income" else "red"
        amount_display = f"{transaction['amount'] / 100:.2f}"
        table.add_row(
            transaction["date"],
            f"[{color}]{transaction['type']}[/{color}]",
            transaction["category"],
            transaction["description"],
            f"[{color}]{amount_display}[/{color}]",
        )
    console.print(table)


def get_balance():
    """Calculates and displays the balance for the current month."""
    transactions = read_transactions()
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

    console = Console()
    balance_text = f"Balance: {balance / 100:.2f}"
    color = "green" if balance >= 0 else "red"

    console.print(f"Total Income: [green]{total_income / 100:.2f}[/green]")
    console.print(f"Total Expenses: [red]{total_expenses / 100:.2f}[/red]")
    console.print(f"[{color}]{balance_text}[/{color}]")
