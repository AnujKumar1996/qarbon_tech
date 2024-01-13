from fastapi import APIRouter, Depends, Response, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from requests.models import Response as reqres
from starlette.responses import JSONResponse
from src.call_external_apis.call_create_attachment_api import \
    call_create_attachment_api
from src.common.exceptions import raise_exception
from src.common.json_read import field_mapping_key_val
from src.common.qcl_error_handling import handle_qcl_error

from .response_headers import add_headers

token = HTTPBearer()

router = APIRouter(
    prefix="/mef/v1/accounting/attachments",
    tags=["QCL Attachment APIs"]
)


@router.post('/upload')
def upload_attachment(header_request:Request, file: UploadFile, response: Response, header_token: str = Depends(token)):
    """
    This endpoint is used to upload the attachment.
    """
    try:
        add_headers(response)
        
        token_type_val = header_token.scheme
        token_val = header_token.credentials
        
        refresh_token = header_request.headers.get("Refreshtoken")
        
        qcl_response = call_create_attachment_api(file, token_val, refresh_token, token_type_val)
        
        response = handle_qcl_error(qcl_response,refresh_token,file,call_create_attachment_api)
       
        if isinstance(response, reqres):
            if response.status_code == 201 or response.status_code == 200:
                qcl_response = response
            else:
                return handle_qcl_error(response,refresh_token,file,call_create_attachment_api)
        
        elif isinstance(response, JSONResponse):
            return response

        qcl_response = qcl_response.json()
        
        field_json = field_mapping_key_val.get("qcl_cc_order")
        attachment_id_val = qcl_response.get(field_json.get("attachmentId"))
        response_dict = {"attachmentId": attachment_id_val}

        return JSONResponse(status_code=200, content=response_dict, media_type="application/json;charset=utf-8")
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    