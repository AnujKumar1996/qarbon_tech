from typing import Union

from fastapi import APIRouter, Depends, Response, status, Request
from requests.models import Response as reqres
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from src.call_external_apis.call_orders_list_api import call_orders_list_api
from src.common.exceptions import raise_exception
from src.common.json_read import common_schema
from src.field_mapping.map_order_list_fields import map_orders_list_fields
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error422, Error500)
from src.schemas.qcl_cc_schemas.orders_list_schemas import (
    OrdersCYXListResponse, OrdersEQXListResponse, OrdersListObject)
from src.common.qcl_error_handling import handle_qcl_error


token = HTTPBearer()

from .response_headers import add_headers

router = APIRouter(
    prefix="/mef/v1/accounting/orders",
    tags=["Orders APIs"]
)

@router.post('/qcl_order_list',
            response_model = Union[OrdersCYXListResponse, OrdersEQXListResponse, Error400, Error401, Error403, Error404, Error422, Error500],
            responses = {
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                }
            )
def get_order_list(header_request:Request, response: Response, info: OrdersListObject, header_token:str = Depends(token)):
    """
    This endpoint is used to get list of orders.
    """
    try:
        
        refresh_token = header_request.headers.get("Refreshtoken")
        
        
        token_type_val = header_token.scheme
        token_val = header_token.credentials
        
        add_headers(response)
        order_data = info.model_dump(by_alias=True)
        
        is_mapped, msg_statuscode, mapped_data, reason, reference_error, message_code, property_path = map_orders_list_fields(order_data)
        
        if not is_mapped and isinstance(mapped_data, str):
            return raise_exception(msg_statuscode, mapped_data, reason, reference_error, message_code, property_path)
        
        qcl_response = call_orders_list_api(mapped_data, token_val, refresh_token, token_type_val)
        
        response = handle_qcl_error(qcl_response,refresh_token,mapped_data,call_orders_list_api)
       
        if isinstance(response, reqres):
            if response.status_code == 201 or response.status_code == 200:
                qcl_response = response
            else:
                return handle_qcl_error(response,refresh_token,mapped_data,call_orders_list_api)
        
        elif isinstance(response, JSONResponse):
            return response
             
        qcl_response = qcl_response.json()

        destination_id = info.genericData.destinationId
        
        if destination_id == "EQX":
            response_data = jsonable_encoder(OrdersEQXListResponse(**qcl_response))
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                content = response_data,
                media_type="application/json;charset=utf-8"
                )
            
        elif destination_id == "CYX":
            response_data = jsonable_encoder(OrdersCYXListResponse(**qcl_response))
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                content = response_data,
                media_type = "application/json;charset=utf-8"
                )
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

