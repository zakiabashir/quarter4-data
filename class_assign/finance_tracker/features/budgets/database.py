from typing import Dict

BUDGETS_FILE = "database/budgets.txt"

def read_budgets() -> Dict[str, int]:
    """Reads all budgets from the file."""
    budgets = {}
    try:
        with open(BUDGETS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                budgets[parts[0]] = int(parts[1])
    except FileNotFoundError:
        return {}
    return budgets

def write_budgets(budgets: Dict[str, int]):
    """Writes all budgets to the file."""
    with open(BUDGETS_FILE, "w") as f:
        for category, amount in budgets.items():
            f.write(f"{category}|{amount}\n")

def add_budget(category: str, amount: int):
    """Adds or updates a budget for a category."""
    budgets = read_budgets()
    budgets[category] = amount
    write_budgets(budgets)
