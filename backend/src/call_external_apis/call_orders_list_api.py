import json

import requests
from src.common.json_read import properties


def call_orders_list_api(request_body, token, refresh_token, token_type):
    """
    Function to call the corresponding qcl API with access token.
    """
    try:
        base_url = properties.get('origin').get('origin_2')
    except Exception as e:
        return str(e)

    api_url = base_url+"accounting/orders/qcl_order_list"

    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"{token_type} {token}",
        "RefreshToken" : f"{refresh_token}"
    }
    
    response = requests.post(api_url, data=json.dumps(request_body), headers=headers)
    return response
