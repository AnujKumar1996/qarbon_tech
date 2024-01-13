from fastapi import APIRouter, Response, Query, status
from typing import Union ,Optional
from pathlib import Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .response_headers import add_headers
from src.schemas.sonata_schemas.appointment_schemas import Appointment_Create,Appointment, Appointment_Find, Appointment_Update
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error422,Error409)
from src.appointment_operations.create_appointment import create_appointment
from src.appointment_operations.retrieves_appointment_by_id import retrieve_appointment_by_id
from src.appointment_operations.retrieves_appointment_list import retrieve_appointment_list
from src.appointment_operations.change_inflight_appointment import change_inflight_appointment
from src.common.exceptions import raise_exception
router=APIRouter(prefix="/v1/MEF/lsoSonata/appointment",
                 tags=["Appointment"])

@router.post('/appointment',
            response_model=Union[Appointment, Error400, Error401,Error404, Error403, Error422, Error500],
            status_code=201,
            responses={
                201: common_schema["response_appointment_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                422: common_schema["response_422"]
                }
            )
async def create_an_appointment(
    order:Appointment_Create,
    response:Response,
     buyerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer. \
            Reference: MEF 79 (Sn 8.8)",
        ),

    sellerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when the responding entity represents more than one Seller. \
            Reference: MEF 79 (Sn 8.8)"
        )
    ):
    """
    A request initiated by the Buyer to create a Appointment in the Seller's system to report an Issue experienced by the Buyer.
    """
    add_headers(response)
    try:
        return create_appointment(order, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
        

@router.get('/appointment/{id}',
            response_model=Union[Appointment, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["response_appointment_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
                
                }
            )
async def retrieves_an_appointment_by_id(
    response: Response,
    id: str = Path(description = "Unique (within the Seller domain) identifier for the Appointment."),
    buyerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer. \
            Reference: MEF 79 (Sn 8.8)",
        ),

    sellerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when the responding entity represents more than one Seller. \
            Reference: MEF 79 (Sn 8.8)"
        )
    ):
    
    try:
        add_headers(response)
        
        return retrieve_appointment_by_id(id, buyerId, sellerId)
    
    except Exception as err:
                return raise_exception(status_msg_code=500,
                                    message= str(err), 
                                    reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                    reference_error=None, 
                                    message_code="internalError", 
                                    property_path=None) 

    



@router.get('/appointment',
            response_model=Union[Appointment_Find, Error400, Error401,Error404, Error403, Error422, Error500],
            status_code=200,
            responses={
                200: common_schema["retrieves_appointment_list_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                500: common_schema["response_500"]
            }
            ) 
async def list_or_found_appointment_objects(
    response: Response,
    
    workOrderId: Optional[str] = Query(
        "",
        description="A reference to a WorkOrder for which the Appointment is created.",
    ),
    
    validFor_gt:Optional[str] = Query(
        None,
        description="The Date and Time the Appointment is confirmed to start and end - greater than.",
        alias="validFor.gt",
        format="date-time",
    ),
    validFor_lt:Optional[str] = Query(
        None,
        description="The Date and Time the Appointment is confirmed to start and end - lower than.",
        alias="validFor.lt",
        format="date-time",
    ),
    status:Optional[str] = Query(
        "",enum=["confirmed", "inProgress", "cancelled", "missed", "failed", "completed"],
        description="A site identifier that is associated with the Appointment.",
    ),
    geographicalSiteId: Optional[str] = Query(
        "",
        description="A site identifier that is associated with the Appointment.",
    ),
    geographicalAddressId: Optional[str] = Query(
        "",
        description="An address identifier that is associated with the Appointment.",
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer. Must be specified in the request only when the requester represents more than one Buyer.",
    ),

    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. Must be specified in the request only when the responding entity represents more than one Seller.",
    ),

    offset: Optional[int] = Query(
        None,
        description="Requested index for the start of resources to be provided in response.",
    ),

    limit: Optional[int] = Query(
        None,
        description="Requested number of resources to be provided in response.",
        format="int32",
    )
    ):
    """
    The Buyer requests a list of Appointment from the Seller based on a set of specified filter criteria. The Seller returns a summarized list of Appointments.
    """
    try:        
            add_headers(response)  
            
            return retrieve_appointment_list(workOrderId, status, validFor_gt, validFor_lt, geographicalSiteId, geographicalAddressId,buyerId, sellerId, offset, limit)

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
 
 
@router.patch('/appointment/{id}',
            response_model=Union[Appointment, Error400, Error401,Error404, Error403, Error500,Error409, Error422],
            status_code=200,
            responses={
                200: common_schema["response_appointment_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                409: common_schema["response_409"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                
                }
            )
async def updates_partially_an_appointment(
    order:Appointment_Update,
    response: Response,
    id: str = Path(description = "Unique (within the Seller domain) identifier for the Appointment."),
    buyerId: str = Query("", 
                description="The unique identifier of the organization that is acting \
                as the a Buyer. MUST be specified in the request only when the requester \
                represents more than one Buyer. Reference: MEF 79 (Sn 8.8)"),
    
    sellerId: str = Query("", 
                description="The unique identifier of the organization that is acting as\
                the Seller. MUST be specified in the request only when responding entity \
                represents more than one Seller. Reference: MEF 79 (Sn 8.8)")


    ):
    """
    This operation updates partially a Appointment entity.
    """
    add_headers(response)
    
    try:

        return change_inflight_appointment(order, id, buyerId, sellerId)
    
    except Exception as err:
                return raise_exception(status_msg_code=500,
                                    message= str(err), 
                                    reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                    reference_error=None, 
                                    message_code="internalError", 
                                    property_path=None) 



