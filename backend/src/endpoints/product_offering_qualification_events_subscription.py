from typing import Union
from pathlib import Path
from fastapi import APIRouter, Query, Response
from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error501)
from src.schemas.sonata_schemas.common_schemas import (EventSubscription,
                                                       EventSubscriptionInput)
from .response_headers import add_headers
from src.common.exceptions import raise_exception

from src.product_offering_qualification_operations.subscribe_productoffering_qualification_notifications import  subscribe_productoffering_qualification_notifications
from src.product_offering_qualification_operations.unsubscribing_productoffering_qualification_notifications import unsubscribing_productoffering_qualification_notifications
router = APIRouter( 
                   prefix="/v1/MEF/lsoSonata/productOfferingQualification",
                   tags=["productOfferingQualification Events Subscription"]
                   )

@router.post('/hub',
            response_model=Union[EventSubscription, Error400, Error401, Error403, Error404,  Error500,Error501],
            status_code=201,
            responses={
                201: common_schema["hub_response_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )

async def allows_a_buyer_to_register_to_receive_poq_state_change_notifications(
    order: EventSubscriptionInput,
    response: Response,

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
    A request initiated by the Buyer to instruct the Seller to send notifications of POQ create, POQ and/or POQ Item state changes if the Buyer has registered for these notifications. The state change notifications are sent only in the Deferred response scenario as in the Immediate response scenario once the response to POQ Request is provided (create notification), there will be no further state changes
    """
    add_headers(response)
    try:
        return subscribe_productoffering_qualification_notifications(order, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
        

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
async def unregister_listener(
       
    id: str = Path(description = "Identifier of the Hub"),
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
    This operation is used to delete an event subscription
    """
    try:
        
        return unsubscribing_productoffering_qualification_notifications(id, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
     

