from fastapi import APIRouter, Response, Query
from typing import Union
from .response_headers import add_headers
from src.schemas.sonata_schemas.appointment_schemas import SearchTimeSlot_Create, SearchTimeSlot
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403,
                                                         Error500, Error422)
from src.appointment_operations.create_timeslot import create_a_timeslot
from src.common.exceptions import raise_exception
router=APIRouter(prefix="/v1/MEF/lsoSonata/appointment",
                 tags=["SearchTimeSlot"])


@router.post('/SearchTimeSlot',
            response_model=Union[SearchTimeSlot, Error400, Error401, Error403, Error422, Error500],
            status_code=201,
            responses={
                201: common_schema["searchTimeSlot_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                500: common_schema["response_500"],
                422: common_schema["response_422"]
                }
            )
async def creates_a_searchtimeslot(
    order:SearchTimeSlot_Create,
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
        return create_a_timeslot(order, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 

