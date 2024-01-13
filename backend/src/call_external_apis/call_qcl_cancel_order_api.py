import json
import requests
from src.common.json_read import properties


def call_qcl_cancel_order(request_body, token, refresh_token,token_type):
    try:
        base_url = properties.get('origin').get('origin_1')
    except Exception as e:
        return str(e)
        
    api_url = base_url + "qcl_crossconnect_cancel"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"{token_type} {token}",
        "RefreshToken" : f"{refresh_token}"
    }
    
    response = requests.post(api_url, data=json.dumps(request_body), headers=headers)
    return response
