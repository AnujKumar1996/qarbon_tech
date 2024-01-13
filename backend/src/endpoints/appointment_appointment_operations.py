from fastapi import APIRouter,Response,Query
from typing import Union
from pathlib import Path
from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500)
from src.common.exceptions import raise_exception
from src.appointment_operations.cancel_appointment import cancel_appointment

router=APIRouter(prefix="/v1/MEF/lsoSonata/appointment",
                 tags=["Appointment Appointment Operations"])

@router.post('/appointment/{id}',
            response_model=Union[Error400, Error401, Error403,Error404,  Error500],
            response_class=Response,
               responses={
                204: common_schema["response_delete_204"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
              
                }
            )
async def cancels_an_appointment( 
                             
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
    
    """
    This operation sends a cancellation request.
    """
    try:
        
        return cancel_appointment(id, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
     