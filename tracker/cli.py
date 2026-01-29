import argparse
from .service import add_expense
from .utils import valid_date
from pydantic import ValidationError

def common_filter_arguments():
    p =  argparse.ArgumentParser

    p.add_argument("--month", help="Filter by month: YYYY-MM")
    p.add_argument("--from-month", dest="from_month", help="Start month: YYYY-MM")
    p.add_argument("--to-month", dest="to_month", help="End month: YYYY-MM")
    p.add_argument("--category", help="Filter by category ")

def parse_argument():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparser = parser.add_subparsers(dest="command")

    # ---- add ---
    add_parser = subparser.add_parser("add")
    
    add_parser.add_argument("--date", type=valid_date, help="YYYY-MM-DD")
    add_parser.add_argument("--category", required=True, help="e.g:food, transport, rent (lowercase)")
    add_parser.add_argument("--amount", type=float, required=True, help="Value must be greater than 0")
    add_parser.add_argument("--currency", default="BDT", help="e.g:'BDT', 'USD', 'INR'")
    add_parser.add_argument("--note", default="")

    # ----List-----
    list_parser = subparser.add_parser("list")
    common_filter_arguments(list_parser)

    # ---summary---
    summary_parser = subparser.add_parser("summary")
    common_filter_arguments(summary_parser)

    args = parser.parse_args()

    if args.command == "add":
        new_expense = {
            # "id": args.id,
            # "date": args.date,
            "category": args.category,
            "amount": args.amount,
            "currency": args.currency,
            "note": args.note,
        }
        try:
            exp = add_expense(new_expense)
            print(f"Added: {exp.id}")
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                print(f"error: {field}: {err['msg']}")
            return

    elif args.command == "list":
        from .service import list_expense
        expenses = list_expense()

        if not expenses:
            print("No expenses found")
            return
        
        print(f"{'ID':<22} {'Date':<12} {'Category':<10} {'Amount':<10} {'Currency':<10} {'Note'}")
        for e in expenses:
            print(f"{f'[{e.id}]':<22} {e.date:<12} {e.category:<10} {e.amount:<10} {e.currency:<10} {e.note}")
    

if __name__ == "__main__":
    parse_argument()