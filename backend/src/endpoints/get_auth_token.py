from fastapi import APIRouter
from fastapi.security import HTTPBearer

from src.call_external_apis.call_auth_token import get_access_token
from src.schemas.user_model import AuthModel
from src.common.exceptions import raise_exception
from src.order_status_utils.set_env_file import set_env_file

token = HTTPBearer()

router = APIRouter(tags=['authentication'],
                   prefix="/mef/v1")

@router.post("/token")
async def get_token(client: AuthModel):
    try:
        response = await get_access_token(client.clientId, client.clientSecret)

        if response.get("statusCode") == 500 and response.get("body") == '"Cannot Validate"':
            status_msg_code = 401
            message = "Invalid credentials"
            reason = "Invalid clientId or clientSecret"
            reference_error = None
            message_code = "invalidCredentials"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        response_data = response.get("data")
        set_env_file(
            ClientId = client.clientId,
            ClientSecret = client.clientSecret,
            AccessToken = response_data.get("AccessToken"),
            RefreshToken = response_data.get("RefreshToken")
        )
        return response
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
