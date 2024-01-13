from fastapi import APIRouter, Response, Query,Path,status
from typing import Optional
from src.common.json_read import common_schema
from src.trouble_ticket_operations.cancel_troubleticket_by_id import cancel_troubleticket_by_id
from src.trouble_ticket_operations.closes_troubleticket_by_id import closes_troubleticket_by_id
from src.trouble_ticket_operations.reopen_troubleticket_by_id import reopen_troubleticket_by_id
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.trouble_ticket_schema import Reason


router=APIRouter(prefix="/v1/MEF/lsoSonata/troubleTicket",
                 tags=["Trouble Ticket operations"])

@router.post("/troubleTicket/{id}/cancel",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "Cancelled"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })
def cancels_a_trouble_ticket(
    
    id: str = Path(
        description="Identifier of the TroubleTicket"
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer.\
                    Must be specified in the request only when the requester represents more than one Buyer."
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller.\
                     Must be specified in the request only when the responding entity represents more than one Seller."
    ),
):
    
    """
    This operation sends a cancellation request.
    """
    
    try:
        return cancel_troubleticket_by_id(id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/troubleTicket/{id}/close",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "Closed"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })
def closes_a_trouble_ticket(
    
    id: str = Path(
        description="Identifier of the TroubleTicket"
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer.\
                    Must be specified in the request only when the requester represents more than one Buyer."
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller.\
                     Must be specified in the request only when the responding entity represents more than one Seller."
    ),
):
    
    """
    This operation allows the Buyer to send Ticket Resolution Confirmation by closing it
    """
    
    try:
        return closes_troubleticket_by_id(id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/troubleTicket/{id}/reopen",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "Reopened"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })
def closes_a_trouble_ticket(
    order: Reason,
    id: str = Path(
        description="Identifier of the TroubleTicket"
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer.\
                    Must be specified in the request only when the requester represents more than one Buyer."
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller.\
                     Must be specified in the request only when the responding entity represents more than one Seller."
    ),
):
    
    """
    The operation allows the Buyer to send Ticket Resolution Confirmation by reopening it
    """
    
    try:
        return reopen_troubleticket_by_id(order,id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

