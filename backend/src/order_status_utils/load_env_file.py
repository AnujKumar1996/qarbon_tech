import os
from dotenv import load_dotenv

def load_env_file() -> None:
    """
    Load clientId and clientSecret from a .env file.

    Returns:
    - None
    """

    try:    
        # Load environment variables from .env file
        load_dotenv()

        # get environment variables

        access_token = os.getenv('AccessToken')
        refresh_token = os.getenv('RefreshToken')

        client_id = os.getenv('ClientId')
        client_secret = os.getenv('ClientSecret')

        return access_token, refresh_token, client_id, client_secret

    except Exception as e:
        print(e)
        return None, None, None, None
