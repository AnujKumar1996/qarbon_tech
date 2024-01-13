import json
from pathlib import Path

def create_response_json(unique_id, data_dict, file_location):
    """
    Method to write responses to json file
    """
    try:
        with open(file_location, 'r') as file:
            existing_data = json.load(file)
    except Exception:
        existing_data = {}
    
    existing_data[unique_id] = data_dict
    
    try:
        with open(file_location, 'w') as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data for unique ID {unique_id} has been written to {file_location}")
    except Exception as e:
        print(f"An error occurred while writing to {file_location}: {e}")


def update_state(id,new_data, filename):
    """
    Method to update responses to json file
    """
    
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[id]["state"] = new_data
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent = 4)

def update_subscription(id,new_data, filename):
     with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[id]["subscription"] = new_data
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent = 4) 

def delete_record(id, filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        if id in file_data:
            del file_data[id]
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=4) 

def update_lattice_id(transaction_id, request_type):
    """
    Function to update JSON with generated lattice_transaction_id. 
    """
    current_directory = Path(__file__).parents[1]
    file_location = current_directory / 'transaction_ids/transaction_id.json' 
    
    try:
        with open(file_location, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "order": [],
            "cancel": [],
            "move": []
            }

    if transaction_id not in data[request_type]:
        # If lattice_transaction_id doesn't exist, add it to the list.
        data[request_type].append(transaction_id)
    
    try:
        with open(file_location, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        return False
