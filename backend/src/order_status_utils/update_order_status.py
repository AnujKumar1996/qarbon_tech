import json

from pathlib import Path

from src.common.json_read import qcl_states

def update_order_status(lattice_transaction_id, request_type, status):
    """
    Function to update the state of a specific order response based on QCL status. 
    """
    try:
        qcl_status = None

        all_qcl_status = qcl_states.get('all_states', {})

        for key, status_list in all_qcl_status.items():
            
            if status in status_list:
                qcl_status = key
                break

        if qcl_status:
            file_map = qcl_states.get('file_map', {})
            response_file_name = file_map.get(request_type)
            file_name = Path(__file__).parents[1] / 'responses' / response_file_name

            with open(file_name, 'r+') as json_file_object:
                updated_json_data = json.load(json_file_object)

                if lattice_transaction_id in updated_json_data.keys():

                    if updated_json_data[lattice_transaction_id]['state'] != qcl_status:
                    
                        updated_json_data[lattice_transaction_id]['state'] = qcl_status

                        # Move the file cursor to the beginning before writing
                        json_file_object.seek(0)
                        json.dump(updated_json_data, json_file_object, indent=4)

                        # Truncate the file in case the new content is shorter than the old content
                        json_file_object.truncate()
        
    except Exception as e:
        print(e)
