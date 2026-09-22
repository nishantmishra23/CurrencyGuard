# utils/formatters.py

def format_currency(amount, currency_code=""):
    """Format amount as a string with commas and 2 decimal places."""
    return f"{amount:,.2f} {currency_code}".strip()

def format_percentage(value):
    """Format percentage with +/- sign."""
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:.2f}%"
