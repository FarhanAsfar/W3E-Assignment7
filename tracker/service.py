from .models import Expense
from .storage import exist_dir, load_data, save_data
from datetime import datetime, date
from typing import Optional
from pydantic import ValidationError

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

    return f"EXP-{date}-{last_serial+1:04d}"


def month_start_from_yyyy_mm(yyyy_mm):
    return datetime.strptime(yyyy_mm, "%Y-%m").replace(day=1)

def month_start_from_yyyy_mm_dd(yyyy_mm_dd):
    d = datetime.strptime(yyyy_mm_dd, "%Y-%m-%d")
    return d.replace(day=1)


def apply_common_filters(
        expenses: [Expense],
        month: Optional[str] = None,
        from_month: Optional[str] = None,
        to_month: Optional[str] = None,
        category: Optional[str] = None,
):
    #category
    if category:
        c = category.strip().lower()
        expenses = [e for e in expenses if e.category.strip().lower() == c]
    
    if month:
        target = month_start_from_yyyy_mm(month)
        expenses = [e for e in expenses if month_start_from_yyyy_mm_dd(e.date) == target]


    # month range
    if from_month and to_month:
        start = month_start_from_yyyy_mm(from_month)
        end = month_start_from_yyyy_mm(to_month)
        if start > end:
            raise ValueError("--from-month cannot be after --to-month")
        expenses = [
            e for e in expenses
            if start <= month_start_from_yyyy_mm_dd(e.date) <= end
        ]

    return expenses


# --- argument command execution ----
def add_expense(expense_data):
    data = load_data()
    expenses = data.get("expenses", [])

    if not expense_data.get("date"):
        expense_data["date"] = date.today().strftime("%Y-%m-%d")

    new_expense_id = generate_expense_id(expenses)

    # taking all key-value pairs from expense_data and adding a new key "id" with 'new_expense_id' value.
    expense_data = {**expense_data, "id": new_expense_id}

    expense = Expense(**expense_data) # equivalent to expense = Expense("id" = EXP..., "category"=""...)

    expenses.append(expense.model_dump(mode='json'))
    data["expenses"] = expenses

    save_data(data)

    return expense

def list_expense(
        month: Optional[str] = None,
        from_month: Optional[str] = None,
        to_month: Optional[str] = None,
        category: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        sort_by: str = "date",
        descending: bool = False,
):
    data = load_data()
    
    all_data = data.get("expenses", [])

    expenses = []
    for item in all_data:
        try:
            expenses.append(Expense(**item))
        except ValidationError:
            continue 
    
    expenses = apply_common_filters(
        expenses,
        month=month,
        from_month=from_month,
        to_month=to_month,
        category=category,
    )

    return expenses


def summary(
    month: Optional[str] = None,
    from_month: Optional[str] = None,
    to_month: Optional[str] = None,
    category: Optional[str] = None,
):
    expenses = list_expense(
        month=month,
        from_month=from_month,
        to_month=to_month,
        category=category,
    )

    total = 0.0
    by_category = {}

    for e in expenses:
        total += e.amount
        by_category[e.category] = by_category.get(e.category, 0.0) + e.amount

    # stable output
    by_category = dict(sorted(by_category.items(), key=lambda kv: kv[0].lower()))

    return {
        "count": len(expenses),
        "total": total,
        "by_category": by_category,
        "month": month,
        "from_month": from_month,
        "to_month": to_month,
        "category": category,
    }