from pathlib import Path
from typing import Union
from fastapi import APIRouter, Query, Response
from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error501)
from src.schemas.sonata_schemas.common_schemas import (EventSubscription,
                                                       EventSubscriptionInput)
from .response_headers import add_headers
from src.common.exceptions import raise_exception
from src.catalog_operations.subscribe_catalog_notifications import subscribe_catalog_notifications
from src.catalog_operations.retrive_catalog_subscription import retrive_catalog_subscription
from src.catalog_operations.unsubscribing_catalog_notifications import unsubscribing_catalog_notifications
router = APIRouter( prefix="/v1/MEF/lsoSonata/productCatalog",tags=["Product Catalog Events Subscription"])

@router.post('/hub',
            response_model=Union[EventSubscription, Error400, Error401, Error403,  Error500,Error501],
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

async def create_hub(
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
    This operation sets registration for Notifications.
    """
    add_headers(response)
    try:
        return subscribe_catalog_notifications(order, buyerId, sellerId)
    except Exception as err:
            return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 

@router.get('/hub/{id}', response_model=Union[EventSubscription, Error400, Error401, Error403,Error404,  Error500,Error501],
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

async def retrieves_hub_by_id(
    response: Response,
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
    This operation retrieves a hub entity.
    """
    add_headers(response)
    try:
        return retrive_catalog_subscription(id, buyerId, sellerId)
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
    Resets the communication endpoint address the service instance must use to deliver information about its health state, execution state, failures and metrics.
    """
    try:
        return unsubscribing_catalog_notifications(id, buyerId, sellerId)
    except Exception as err:
           return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 

