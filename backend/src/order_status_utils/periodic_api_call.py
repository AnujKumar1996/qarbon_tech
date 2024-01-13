import asyncio
import json

from pathlib import Path

from src.common.json_read import properties, qcl_states
from src.call_external_apis.call_auth_token import get_access_token
from src.call_external_apis.call_transaction_api import call_transaction_api

from .load_env_file import load_env_file
from .set_env_file import set_env_file
from .update_order_status import update_order_status

async def fetch_lattice_state(terminal_states):
    """
    Update the lattice transaction id list based on API response and status.

    Retrieves lattice transaction IDs, makes API calls to obtain their status,
    updates the order status, and stores the updated lattice transaction IDs in a JSON file.

    Returns:
    None: The function updates the lattice transaction id list and does not return a value.
    """

    from .get_lattice_id import get_lattice_id
    try:

        access_token, refresh_token, client_id, client_secret = load_env_file()

        if access_token and refresh_token and client_id and client_secret:
            lattice_transaction_ids = get_lattice_id()

            for request_type, lattice_id_list in lattice_transaction_ids.items():
                updated_list = []

                for lattice_id in lattice_id_list:
                    api_response = call_transaction_api(lattice_id, access_token, refresh_token)
                    response_code = api_response.status_code

                    if response_code == 200:
                        api_response = api_response.json()
                        qcl_item_details = api_response.get('item_details')
                        if qcl_item_details:

                            lattice_qcl_status = qcl_item_details[0].get('qcl_item_status_message')
                            update_order_status(lattice_id, request_type, lattice_qcl_status)

                            if lattice_qcl_status not in terminal_states:
                                updated_list.append(lattice_id)
                        else:
                            updated_list.append(lattice_id)

                    elif response_code in {400, 422, 500}:
                        updated_list.append(lattice_id)

                    elif response_code == 404:
                        json_response = api_response.json()

                        # If lattice_transaction_id not found in QCL database.
                        if 'detail' in json_response:
                            print(json_response.get('detail'))
                        else:
                            updated_list.append(lattice_id)
                            print(json_response.get('message'))

                    elif response_code == 401 and api_response.json().get('message') == "Unauthorized":
                        updated_list.append(lattice_id)

                        json_response = await get_access_token(client_id, client_secret)
                        if not json_response.get("statusCode") == 500:
                            response_data = json_response.get("data")

                            set_env_file(AccessToken = response_data.get("AccessToken"),
                                        RefreshToken = response_data.get("RefreshToken"))
                        else:
                            print("Unable to call '/mef/v1/token' API")

                if lattice_id_list != updated_list and updated_list:
                    file_path = Path(__file__).parents[1] / 'transaction_ids' / 'transaction_id.json'
                    with open(file_path, 'r+') as json_file_object:
                        updated_json_data = json.load(json_file_object)
                        updated_json_data[request_type] = updated_list

                        # Move the file cursor to the beginning before writing
                        json_file_object.seek(0)
                        json.dump(updated_json_data, json_file_object, indent=4)

                        # Truncate the file in case the new content is shorter than the old content
                        json_file_object.truncate()

        else:
            print("Invalid credentials")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def periodic_api_call():
    """
    Function to call the 'transaction/item_details/{lattice_transaction_id}' for each order in time interval.
    """

    time_interval = properties.get('time_interval')
    terminal_states = qcl_states.get('terminal_states')
    
    while True:

        await fetch_lattice_state(terminal_states)
        await asyncio.sleep(time_interval)