from typing import Union, Optional
from fastapi import APIRouter, Query, Response, Path
from src.trouble_ticket_operations.create_troubleticket_hub import subscribe_trouble_ticket_notifications
from src.trouble_ticket_operations.unsubscribe_trouble_ticket_hub import unsubscribe_trouble_ticket
from src.trouble_ticket_operations.retrieves_trouble_ticket_hub import retrieves_trouble_ticket

from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error501)
from src.schemas.sonata_schemas.common_schemas import (EventSubscription,
                                                       EventSubscriptionInput)
from .response_headers import add_headers
from src.common.exceptions import raise_exception
router = APIRouter( prefix="/v1/MEF/lsoSonata/troubleTicket",tags=["Trouble Ticket Events Subscription"])

@router.post('/hub',
            response_model=Union[EventSubscription, Error400, Error401, Error403,  Error500, Error501],
            status_code=201,
            responses={
                201: common_schema["hub_response_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )

async def allows_the_buyer_to_register_to_trouble_ticket_state_change_notifications(
    order: EventSubscriptionInput,
    response: Response,
    buyerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer.",
        ),

    sellerId: Optional[str] = Query(
        
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when responding entity represents more than one Seller."
        )
    ):
    """
    The Buyer requests to subscribe to Ticket and Incident Notifications.
    """
    add_headers(response)
    try:
        return subscribe_trouble_ticket_notifications(order, buyerId, sellerId)
    except Exception as err:
            return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 



@router.delete('/hub/{id}',response_model=Union[Error400, Error401, Error403,Error404,  Error500,Error501],response_class=Response,
               responses={
                204: common_schema["response_delete_204"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )
async def unregister_a_listener(
       
    id: str = Path(description = "The id of the EventSubscription"),
    buyerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
        ),

    sellerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when responding entity represents more than one Seller."
        )
    ):

    """
    The Buyer requests to unsubscribe from Ticket and Incident Notifications
    """
    try:
        
        return unsubscribe_trouble_ticket(id, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
    
@router.get('/hub/{id}',response_model=Union[Error400, Error401, Error403,Error404,  Error500,Error501],response_class=Response,
               responses={
                200: common_schema["hub_response_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )
async def retrieves_listener_information(
       
    id: str = Path(description = "The id of the EventSubscription"),
    buyerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
        ),

    sellerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when responding entity represents more than one Seller."
        )
    ):

    """
    This operation retrieves a hub entity.
    """
    try:
        return retrieves_trouble_ticket(id, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 

     