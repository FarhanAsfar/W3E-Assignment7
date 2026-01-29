from .models import Expense
from .storage import exist_dir, load_data, save_data
from datetime import datetime

def date_str():
    return datetime.now().strftime("%Y%m%d")

def generate_expense_id(existing_expenses):
    """
    Expense ID format: EXP-YYYYMMDD-####
    """
    date = date_str()

    if not existing_expenses:
        return f"EXP-{date}-0001"
    
    last_id = existing_expenses[-1].get("id", "")

    try:
        last_serial = int(last_id.split("-")[-1])
    except Exception:
        last_serial = 0

    return f"EXP-{date}-{last_serial+1: 04d}"

def add_expense():
    exist_dir()