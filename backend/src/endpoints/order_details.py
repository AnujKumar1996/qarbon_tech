from typing import Union
from requests.models import Response as reqres
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from src.call_external_apis.call_qcl_order_details import call_qcl_order_details_api
from src.common.exceptions import raise_exception
from src.common.json_read import common_schema
from src.field_mapping.map_order_details import map_order_details_fields
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,Error403,
                                                         Error422,Error404, Error500)
from src.schemas.qcl_cc_schemas.order_details_schemas import \
    QclOrderDetails
from src.schemas.qcl_cc_schemas.order_details_response_schemas import EYX_Order_details,CQX_Order_details
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.qcl_error_handling import handle_qcl_error


token = HTTPBearer()

from .response_headers import add_headers

router = APIRouter(
    prefix="/mef/v1/accounting/orders"
)

@router.post('/qcl_order_details', tags=["Orders APIs"],
            response_model = Union[EYX_Order_details,CQX_Order_details,Error400, Error401,Error403,Error404, Error422, Error500],
            responses = {
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                400: common_schema["response_404"],
                500: common_schema["response_500"]
                }
            )
def get_order_details(header_request: Request, response: Response, info: QclOrderDetails, header_token:str =Depends(token)):
    """
    This endpoint is used to get details of a Order
    """
    
    try:
        token_type_val = header_token.scheme
        token_val = header_token.credentials
        
        refresh_token = header_request.headers.get("Refreshtoken")
        
        add_headers(response)
        order_data = info.model_dump(by_alias=True)
        
        is_mapped, msg_statuscode, mapped_data, reason, reference_error, message_code, property_path = map_order_details_fields(order_data)

        if not is_mapped and isinstance(mapped_data, str):
            return raise_exception(msg_statuscode, mapped_data, reason, reference_error, message_code, property_path)

        qcl_response = call_qcl_order_details_api(mapped_data, token_val, refresh_token, token_type_val)
        
        
        response = handle_qcl_error(qcl_response,refresh_token,mapped_data,call_qcl_order_details_api)
       
        if isinstance(response, reqres):
            if response.status_code == 201 or response.status_code == 200:
                qcl_response = response
            else:
                return handle_qcl_error(response,refresh_token,mapped_data,call_qcl_order_details_api)
        
        elif isinstance(response, JSONResponse):
            return response
        
        destinationID = info.genericData.destinationId
        
        if destinationID == "EQX":
            response_data1 = jsonable_encoder(EYX_Order_details(**qcl_response.json()))
            return JSONResponse(status_code=status.HTTP_200_OK,
                content=response_data1,
                media_type="application/json;charset=utf-8"
                )
            
        elif destinationID == "CYX":
            response_data1 = jsonable_encoder(CQX_Order_details(**qcl_response.json()))
            return JSONResponse(status_code=status.HTTP_200_OK,
                content=response_data1,
                media_type="application/json;charset=utf-8"
                )
            
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

