import argparse
from .storage import create_expense

def parse_argument():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add")
    list_parser = subparser.add_parser("list")


    # add_parser.add_argument("--id", required=True)
    add_parser.add_argument("--date", required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--currency", required=True)
    add_parser.add_argument("--note", default="")

    args = parser.parse_args()

    if args.command == "add":
        new_expense = {
            # "id": args.id,
            "date": args.date,
            "category": args.category,
            "amount": args.amount,
            "currency": args.currency,
            "note": args.note,
        }
        create_expense(new_expense)
    elif args.command == "list":
        from .storage import list_expenses
        list_expenses()
    

if __name__ == "__main__":
    parse_argument()