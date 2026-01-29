from datetime import datetime
import argparse

def valid_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format")