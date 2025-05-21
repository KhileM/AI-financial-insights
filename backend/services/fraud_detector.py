def is_fraudulent(transaction_data):
    """
    Mock logic:
    - Flags transactions over $10,000 as fraudulent.
    """
    amount = transaction_data.get("amount", 0)
    return amount > 10000