import argparse
from .service import add_expense,list_expense,summary
from .utils import valid_date
from pydantic import ValidationError
from .logger import logger

def common_filter_arguments(p: argparse.ArgumentParser):
    p.add_argument("--month", help="Filter by month: YYYY-MM")
    p.add_argument("--from-month", dest="from_month", help="Start month: YYYY-MM")
    p.add_argument("--to-month", dest="to_month", help="End month: YYYY-MM")
    p.add_argument("--category", help="Filter by category ")


def add_list_only_arguments(p: argparse.ArgumentParser):
    p.add_argument("--min", dest="min_amount", type=float, help="Minimum amount")
    p.add_argument("--max", dest="max_amount", type=float, help="Maximum amount")
    p.add_argument("--sort-by", choices=["date", "amount", "category"], default="date")
    p.add_argument("--desc", action="store_true", help="Sort descending")


def parse_argument():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparser = parser.add_subparsers(dest="command", required=True)

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
    add_list_only_arguments(list_parser)

    # ---summary---
    summary_parser = subparser.add_parser("summary")
    common_filter_arguments(summary_parser)

    # ---delete ---
    delete_parser = subparser.add_parser("delete")
    delete_parser.add_argument("--id", required=True, help="Expense ID (e.g: EXP-YYYYMMDD-0001)")

    # ---edit ---
    edit_parser = subparser.add_parser("edit")
    edit_parser.add_argument("--id", required=True, help="Expense ID (e.g: EXP-YYYYMMDD-0001)")
    edit_parser.add_argument("--date", type=valid_date, help="YYYY-MM-DD")
    edit_parser.add_argument("--category", help="e.g:food, transport, rent")
    edit_parser.add_argument("--amount", type=float, help="Value must be greater than 0")
    edit_parser.add_argument("--currency", help="e.g:'BDT', 'USD', 'INR'")
    edit_parser.add_argument("--note", help="")

    args = parser.parse_args()

    logger.info(f"Command started: {args.command}")

    def validate_filters():
        if args.month and (args.from_month or args.to_month):
            parser.error("use either --month OR --from-month/--to-month, not both")
        if (args.from_month and not args.to_month) or (args.to_month and not args.from_month):
            parser.error("use both --from-month and --to-month together")

    if args.command in ("list", "summary"):
        validate_filters()

    if args.command == "add":
        new_expense = {
            "date": args.date,
            "category": args.category,
            "amount": args.amount,
            "currency": args.currency,
            "note": args.note,
        }
        try:
            exp = add_expense(new_expense)
            print(f"Added: {exp.id}")
            logger.info(f"ADD success | id={exp.id} amount={exp.amount} category={exp.category}")
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                print(f"error: {field}: {err['msg']}")
            return

    elif args.command == "list":        
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
            logger.info(f"LIST success | count={len(expenses)}")
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                print(f"error: {field}: {err['msg']}")
            return
        except ValueError as e:              
            print(f"error: {e}")
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
        logger.info(
            f"SUMMARY success | count={result.get('count')} total={result.get('total')}"
        )

        print(f"Total Expenses: {result.get('count', 0)}")
        print(f"Grand Total: {result.get('total', 0.0)}")
        by_category = result.get("by_category", {})
        if by_category:
            print("\nBy category:")
            for k, v in by_category.items():
                print(f"  {k}: {v}")

    elif args.command == "delete":
        from .service import delete_expense 
        ok = delete_expense(args.id)
        if ok:
            print(f"Deleted: {args.id}")
            logger.info(f"DELETE success | id={args.id}")
        else:
            print(f"error: expense not found: {args.id}")
            logger.warning(f"DELETE failed | id not found={args.id}")

    elif args.command == "edit":
        from .service import edit_expense

        updates = {}
        if args.date is not None:
            updates["date"] = args.date
        if args.category is not None:
            updates["category"] = args.category
        if args.amount is not None:
            updates["amount"] = args.amount
        if args.currency is not None:
            updates["currency"] = args.currency
        if args.note is not None:
            updates["note"] = args.note

        if not updates:
            print("error: nothing to update (provide at least one field)")
            return

        try:
            updated = edit_expense(args.id, updates)
            if updated:
                print(f"Updated: {args.id}")
                logger.info(f"EDIT success | id={args.id} fields={list(updates.keys())}")
            else:
                print(f"error: expense not found: {args.id}")
                logger.warning(f"EDIT failed | id not found={args.id}")
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                print(f"error: {field}: {err['msg']}")
            return
        
if __name__ == "__main__":
    parse_argument()