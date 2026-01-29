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



def add_expense(expense_data):
    data = load_data()
    expenses = data.get("expenses", [])

    new_expense_id = generate_expense_id(expenses)

    # taking all key-value pairs from expense_data and adding a new key "id" with 'new_expense_id' value.
    expense_data = {**expense_data, "id": new_expense_id}

    expense = Expense(**expense_data) # equivalent to expense = Expense("id" = EXP..., "category"=""...)

    expenses.append(expense.model_dump(mode='json'))
    data["expenses"] = expenses

    save_data(data)

    return expense

def list_expense():
    data = load_data()
    
    all_data = data.get("expenses", [])

    expenses = [Expense(**e) for e in all_data]

    return expenses