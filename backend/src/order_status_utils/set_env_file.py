import os
def set_env_file(**dict_data):
    """
    Set clientId and clientSecret in environment variables and persist them to a .env file.

    Parameters:
    - client_id (str): The clientId to be set.
    - client_secret (str): The clientSecret to be set.

    Returns:
    - None
    """


    for key, value in dict_data.items():
        if value:
            os.environ[key] = value
