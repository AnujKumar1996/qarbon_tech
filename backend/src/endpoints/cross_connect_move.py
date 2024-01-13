from typing import Union
from requests.models import Response as reqres
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from src.call_external_apis.call_qcl_move_api import call_qcl_move_api
from src.common.exceptions import raise_exception
from src.common.extract_error_message import extract_error_msg
from src.common.json_read import common_schema, field_mapping_key_val
from src.field_mapping.map_move_fields import map_move_fields
from src.schemas.interlude_schemas.error_schemas import (Error400, Error404,
                                                         Error422, Error500)
from src.schemas.qcl_cc_schemas.cross_connect_move_schemas import \
    QclCrossConnectMoveObject
from src.common.create_jsonfile import update_lattice_id
from src.common.qcl_error_handling import handle_qcl_error



token = HTTPBearer()

from .response_headers import add_headers

router = APIRouter(
    prefix="/mef/v1/accounting/crossconnect"
)

@router.post('/qcl_crossconnect_move', tags=["QCL Crossconnect API"],
            response_model = Union[Error400, Error404, Error422, Error500],
            responses = {
                400: common_schema["response_400"],
                404: common_schema["response_404"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                }
            )
def move_cross_connect_order(response: Response, header_request:Request, info: QclCrossConnectMoveObject, header_token:str =Depends(token)):
    """
    This endpoint is used to move a cross connect order.
    """
    try:
        refresh_token = header_request.headers.get("Refreshtoken")
        
        add_headers(response)
        order_data = info.model_dump(by_alias=True)
        
        token_type_val = header_token.scheme
        token_val = header_token.credentials

        is_mapped, msg_statuscode, mapped_data, reason, reference_error, message_code, property_path = map_move_fields(order_data)
        
        if not is_mapped and isinstance(mapped_data, str):
            return raise_exception(msg_statuscode, mapped_data, reason, reference_error, message_code, property_path)
        
        qcl_response = call_qcl_move_api(mapped_data, token_val, refresh_token, token_type_val)

        response = handle_qcl_error(qcl_response,refresh_token,mapped_data,call_qcl_move_api)
    
        if isinstance(response, reqres):
            if response.status_code == 201:
                qcl_response = response
            else:
                return handle_qcl_error(response,refresh_token,mapped_data,call_qcl_move_api)
        
        elif isinstance(response, JSONResponse):
            return response
    
        qcl_response = qcl_response.json()

        field_json = field_mapping_key_val.get("qcl_cc_order")
        trancsation_id_val = qcl_response.get(field_json.get("latticeTransactionId"))

        if not update_lattice_id(trancsation_id_val, 'move'):
            status_msg_code = 422
            message = f"Unable to update JSON file with lattice_transaction_id {trancsation_id_val}"
            reason = "Validation error"
            reference_error = None
            message_code = "otherIssue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        response_dict = {"latticeTransactionId":trancsation_id_val}

        return JSONResponse(status_code=201, content=response_dict, media_type="application/json;charset=utf-8")
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

