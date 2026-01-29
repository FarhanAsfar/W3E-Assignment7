import argparse
from .service import add_expense,list_expense,summary
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
        
        try:
            expenses = list_expense(
                month=args.month,
                from_month=args.from_month,
                to_month=args.to_month,
                category=args.category,
                min_amount=args.min_amount,
                max_amount=args.max_amount,
                sort_by=args.sort_by,
                descending=args.desc,
            )
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                print(f"error: {field}: {err['msg']}")
            return
        

        if not expenses:
            print("No expenses found")
            return
        
        print(f"{'ID':<22} {'Date':<12} {'Category':<10} {'Amount':<10} {'Currency':<10} {'Note'}")
        for e in expenses:
            print(f"{f'[{e.id}]':<22} {e.date:<12} {e.category:<10} {e.amount:<10} {e.currency:<10} {e.note}")
    
    elif args.command == "summary":
        result = summary(
            month=args.month,
            from_month=args.from_month,
            to_month=args.to_month,
            category=args.category,
        )

        print(f"Count: {result.get('count', 0)}")
        print(f"Total: {result.get('total', 0.0)}")
        by_category = result.get("by_category", {})
        if by_category:
            print("\nBy category:")
            for k, v in by_category.items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    parse_argument()