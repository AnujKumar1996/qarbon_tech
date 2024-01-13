from fastapi import APIRouter, Response, Query
from typing import Union ,Optional
from pathlib import Path
from .response_headers import add_headers
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500)
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.customer_bill_management_schemas import CustomerBill_Find
from src.customer_bill_operations.retrive_customer_bill_list import retrive_customer_bill_list
from src.schemas.sonata_schemas.customer_bill_management_schemas import CustomerBill
from src.customer_bill_operations.retrieve_customer_bill_by_id import retrieve_customer_bill_by_id
from src.customer_bill_operations.retrieve_customer_bill_item_by_id import retrieve_customer_bill_item_by_id

router=APIRouter(prefix="/v1/MEF/lsoSonata/customerBillManagement",
                 tags=["customerBill"])

@router.get('/customerBill',
            response_model=Union[CustomerBill_Find, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["customer_bill_list"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
            }
            ) 

async def list_or_find_customer_bill_objects(
    response: Response,
    
    billingAccount_id: Optional[str] = Query(
        "",
        description="An identifier for the Billing Account that is unique within the Seller."
    ),
    
    billingPeriod_startDateTime_lt: Optional[str] = Query(
        None,alias="billingPeriod_startDateTime.lt", format="data_time",
        description="The date the Billing Period started - lower than."
    ),
    
    billingPeriod_startDateTime_gt: Optional[str] = Query(
         None,alias="billingPeriod_startDateTime.gt", format="data_time",
        description="The date the Billing Period started - greater than."
    ),
    
    billingPeriod_endDateTime_lt: Optional[str] = Query(
         None,alias="billingPeriod_endDateTime.lt", format="data_time",
        description="The date the Billing Period ended - lower than."
    ),
    
    billingPeriod_endDateTime_gt: Optional[str] = Query(
         None,alias="billingPeriod_endDateTime.gt", format="data_time",
        description="The date the Billing Period ended - greater than."
    ),
    
    category: Optional[str] = Query(
         "",
        description="The category of Bill. One of the following: - normal - duplicate - trial",
        enum=["normal", "duplicate", "trial"]
    ),
    
    state: Optional[str] = Query(
        "",
        description="The state of the Bill Item.",
        enum=["generated", "paymentDue", "settled"]
    ),
    
    offset: Optional[int] = Query(
        None,
        description="Requested index for start of item to be provided in response requested by the client. Note that the index starts with '0'.",
        alias="offset",
        format="int32",
    ),
    limit: Optional[int] = Query(
        None,
        description="Requested number of items to be provided in response requested by client",
        alias="limit",
        format="int32",),
    ):
    """
    This operation list or find GeographicSite entities.
    """
    try:        
        add_headers(response)  

        return retrive_customer_bill_list(billingAccount_id, billingPeriod_startDateTime_lt, billingPeriod_startDateTime_gt, billingPeriod_endDateTime_lt, billingPeriod_endDateTime_gt,  
                        category, state, offset, limit) 

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
 


@router.get('/customerBill/{id}',
            response_model=Union[CustomerBill, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["customer_bill_get_by_id"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
            }
            ) 

async def retrieves_a_customer_bill_by_id(
    response: Response,
    id: str = Path(description = "Identifier of the CustomerBill"),
    ):
    """
    This operation retrieves a CustomerBill entity.
    """
    try:
        add_headers(response)
        
        return retrieve_customer_bill_by_id(id)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 


@router.get('/customerBillItem/{id}',
            response_model=Union[CustomerBill, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["customer_bill_get_by_id"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
            }
            ) 

async def retrieves_a_customer_bill_item_by_id(
    response: Response,
    id: str = Path(description = "Identifier of the CustomerBillItem"),
    ):
    """
    This operation retrieves a CustomerBillItem entity.
    """
    try:
        add_headers(response)
        
        return retrieve_customer_bill_item_by_id(id)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
