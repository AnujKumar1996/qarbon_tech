import requests

from src.common.json_read import properties

def call_transaction_api(lattice_transaction_id, access_token, refresh_token):
    """
    Function to call the 'transaction/item_details/{lattice_transaction_id}' API and 
    get the status for each order in time interval.
    API and 
    Function get the status for each order in time interval.
    """
    
    try:
        base_url = properties.get('origin').get('origin_2')
    except Exception as e:
        return str(e)

    
    api_url = f'{base_url}transaction/item_details/{lattice_transaction_id}'

    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization" : f"Bearer {access_token}",
        "RefreshToken" : f"{refresh_token}"
    }
    return requests.get(api_url, headers=headers)
    
