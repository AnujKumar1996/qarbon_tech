import json
import requests
from src.common.json_read import properties
from src.common.exceptions import raise_exception

def call_qcl_renew_token_api(refresh_token):
    try:
        base_url = properties.get('auth').get('origin')
    except Exception as e:
        return str(e)
    
    api_url = f'{base_url}renewtoken'

    request_body = {
        "scopes": "refresh_token",
        "username": "jmanlangit@qarbontech.io",
        "refresh_token" : f"{refresh_token}"
    }
        
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    response = requests.post(api_url, data=json.dumps(request_body), headers=headers)
    if response.json().get("statusCode") == 500:
        status_msg_code = 401
        message = "Invalid credentials"
        reason = "Invalid 'RefreshToken'"
        reference_error = None
        message_code = "invalidCredentials"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


    return response
