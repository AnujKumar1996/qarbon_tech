import requests
from src.common.json_read import properties


async def get_access_token(client_id: str, client_secret: str):
    try:
        base_url = properties.get('auth').get('origin')
    except Exception as e:
        return str(e)
    
    api_url = f'{base_url}token'
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "ClientId": client_id,
        "ClientSecret": client_secret
    }
    response = requests.post(api_url, headers=headers)
    
    return response.json()
