import requests

from src.common.json_read import properties

def call_qcl_delete_attachment_api(attachment_id, token, refresh_token,token_type):
    """
    function to call qcl delete API of attachment section.
    """
    
    try:
        base_url = properties.get('origin').get('origin_2')
    except Exception as e:
        return str(e)

    
    base_url = base_url+f'attachments/delete/{attachment_id}'
    
    api_url = base_url
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"{token_type} {token}",
        "RefreshToken" : f"{refresh_token}"
    }
    response = requests.delete(api_url,headers=headers)
    return response