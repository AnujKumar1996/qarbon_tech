import json
import requests
from src.common.json_read import properties


def call_qcl_order_list(request_body, token, refresh_token):
    try:
        base_url = properties.get('origin').get('origin_1')
    except Exception as e:
        return str(e)


    api_url = base_url+"qcl_crossconnect_list"
    
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"{token.scheme} {token.credentials}",
        "RefreshToken" : f"{refresh_token}"
    }
    response = requests.post(api_url, data=json.dumps(request_body), headers=headers)
    
    return response
