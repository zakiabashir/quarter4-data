from rich.console import Console
from rich.text import Text
from rich.bar import Bar
from features.transactions.database import read_transactions

def spending_analytics():
    """Analyzes spending by category and displays a bar chart."""
    transactions = read_transactions()

    spending = {}
    for transaction in transactions:
        if transaction["type"] == "Expense":
            category = transaction["category"]
            amount = transaction["amount"]
            spending[category] = spending.get(category, 0) + amount

    if not spending:
        print("No expense data to analyze.")
        return

    console = Console()
    console.print("\n[bold]Spending by Category[/bold]")

    # Find the maximum spending to scale the bars
    if spending:
        max_spending = max(spending.values())
        for category, amount in spending.items():
            # Calculate the ratio for the bar width
            ratio = amount / max_spending if max_spending > 0 else 0
            bar = Bar(size=50, begin=0, end=50 * ratio, color="red")
            text = Text(f"{category}: {amount / 100:.2f}", justify="left")
            console.print(text)
            console.print(bar)
