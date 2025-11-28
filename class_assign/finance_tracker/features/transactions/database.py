from typing import List, Dict

TRANSACTIONS_FILE = "database/transactions.txt"

def read_transactions() -> List[Dict]:
    """Reads all transactions from the file."""
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                transactions.append({
                    "date": parts[0],
                    "type": parts[1],
                    "category": parts[2],
                    "amount": int(parts[3]),
                    "description": parts[4]
                })
    except FileNotFoundError:
        return []
    return transactions

def write_transactions(transactions: List[Dict]):
    """Writes all transactions to the file."""
    with open(TRANSACTIONS_FILE, "w") as f:
        for t in transactions:
            f.write(f"{t['date']}|{t['type']}|{t['category']}|{t['amount']}|{t['description']}\n")

def add_transaction(transaction: Dict):
    """Adds a single transaction to the file."""
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{transaction['date']}|{transaction['type']}|{transaction['category']}|{transaction['amount']}|{transaction['description']}\n")
