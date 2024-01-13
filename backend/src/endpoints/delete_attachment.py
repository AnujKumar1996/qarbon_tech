from fastapi import (APIRouter,Response, status,Depends, Request)
from requests.models import Response as reqres
from starlette.responses import JSONResponse
from fastapi.security import HTTPBearer


from src.common.json_read import common_schema
from src.call_external_apis.call_qcl_delete_attachment_api import call_qcl_delete_attachment_api
from src.common.exceptions import raise_exception
from src.common.qcl_error_handling import handle_qcl_error


token = HTTPBearer()

router = APIRouter(
    prefix="/mef/v1/accounting/attachments",
    tags=["QCL Attachment APIs"]
)
#API to delate attachment for particular id
@router.delete('/delete/{attachment_id}',response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: common_schema["response_delete_204"],
        400: common_schema["response_400"],
        404: common_schema["response_404"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        500: common_schema["response_500"]
        })
async def delete_attachment(header_request:Request, attachment_id:str,header_token: str = Depends(token)):
    '''API to delete attachment.'''
    try:
        refresh_token = header_request.headers.get("Refreshtoken")
        
        token_type_val = header_token.scheme
        token_val = header_token.credentials
        
        if not attachment_id:
            status_msg_code = 404
            message = "'id' not found"
            reason = "Not a valid id"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        else:
            qcl_response = call_qcl_delete_attachment_api(attachment_id, token_val, refresh_token,token_type_val)
            
            response = handle_qcl_error(qcl_response,refresh_token,attachment_id,call_qcl_delete_attachment_api)
       
            if isinstance(response, reqres):
                if response.status_code == 201 or response.status_code == 204:
                    qcl_response = response
                else:
                    return handle_qcl_error(response,refresh_token,attachment_id,call_qcl_delete_attachment_api)
            
            elif isinstance(response, JSONResponse):
                return response
            
            else:
                Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request",
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)