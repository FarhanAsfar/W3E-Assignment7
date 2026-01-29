import json
import os

file_path = "./data/expenses.json"

# checking if directory exists
def exist_dir():
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

# loading data from the json file
def load_data():
    exist_dir()

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {"version": 1, "expenses": []}
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # making sure that keys exist
    data.setdefault("version", 1)
    data.setdefault("expenses", [])
    return data 

# saving data in the json file
def save_data(data):
    exist_dir()

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
