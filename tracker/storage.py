from .models import Expense
import os
import json

def print_expense():
    file_path = "./data/expenses.json"

    # making sure if path exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    expense1 = Expense (
        id = "001",
        date = "2026-01-28",
        category = "food",
        amount = 333.33,
        note = "lunch"
    )

    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open (file_path, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = [{"version": "1"},]
        
        data.append(expense1.to_dict())

        with open (file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"written to file {file_path}")

    except IOError as e: 
        print(f"Couldn't write to the file {e}")
    
   

