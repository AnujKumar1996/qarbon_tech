import json

from pathlib import Path

def get_lattice_id():

    current_directory = Path(__file__).parents[1]
    file_name = current_directory / 'transaction_ids/transaction_id.json' 
    

    if not file_name.exists():
        print(f"File not found '{file_name}'")
        return {}

    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
            
            if isinstance(data, dict):
                return data
            else: 
                return {}
    
    except json.JSONDecodeError as e:
        print(e)
        return {}
    