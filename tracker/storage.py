from .models import Expense
from datetime import datetime
import os
import json


date_str = datetime.now().strftime("%Y%m%d")
    

def create_expense(expense_data):
    file_path = "./data/expenses.json"

    # making sure if path exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open (file_path, 'r') as json_file:
                data = json.load(json_file)
                #if only one data exist, then wrap it inside []
                if isinstance(data, dict):
                    data = [data]
        else:
            data = {
                "version": 1,
                "expenses": []
            }
        
        #  getting last id from expenses array
        expenses = data.get("expenses", [])
        if expenses:
            last_id = expenses[-1].get('id', 'EXP-202060128-0000')
            try:
                last_serial = int(last_id.split('-')[-1])
            except (ValueError, IndexError):
                last_serial = 0
        else:
            last_serial = 0
        
        new_serial = last_serial + 1
        new_id = f"EXP-{date_str}-{new_serial:04d}"
        expense_data['id'] = new_id
        expense_obj = Expense(**expense_data)

        # appending to 'expenses' array
        data["expenses"].append(expense_obj.model_dump(mode='json'))

        with open (file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"written to file {file_path}")

    except IOError as e: 
        print(f"Couldn't write to the file {e}")
    
   
def list_expenses():
    file_path = "./data/expenses.json"

    if not os.path.exists(file_path):
        print("No data found")
        return
    
    with open (file_path, 'r') as json_file:
        data = json.load(json_file)

    expenses = data[1:]

    for exp in expenses:
        print(f"[{exp['date']}] {exp['category']}: {exp['amount']} {exp['currency']} - {exp['note']}")
