from typing import Union
from fastapi import APIRouter, Query, Response, Path
from src.performance_monitoring_operations.events_subscription.create_hub import create_performance_monitoring_hub
from src.performance_monitoring_operations.events_subscription.delete_hub_by_id import unregister_performance_monitoring_notifications
from src.performance_monitoring_operations.events_subscription.retrieve_performance_monitoring_hub_by_id import get_performance_monitoring_hub_by_id

from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error501)

from src.schemas.sonata_schemas.common_schemas import (EventSubscription,
                                                       EventSubscriptionInput)
from .response_headers import add_headers
from src.common.exceptions import raise_exception

router = APIRouter( prefix="/v1/MEF/lsoInterlude/performanceMonitoring",tags=["Performance Monitoring Events Subscription"])

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

async def register_a_listener(
    order: EventSubscriptionInput,
    response: Response,
    ):
    """
    The Buyer/Client or Administrator requests to subscribe to Performance Monitoring Profile, Performance Monitoring Job and/or Performance Measurement Report Notifications.
    """
    add_headers(response)
    try:
        return create_performance_monitoring_hub(order)
    except Exception as err:
            return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 


@router.delete('/hub/{id}',response_model=Union[Error400, Error401, Error403,Error404,  Error500, Error501],response_class=Response,
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
       
    id: str = Path(description = "The id of the EventSubscription")
    ):
    """
    The Buyer/Client or Administrator requests to unsubscribe from Performance Monitoring Profile, Performance Monitoring Job and/or Performance Measurement Report Notifications
    """
    try:
        return unregister_performance_monitoring_notifications(id)
    except Exception as err:
        return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 


@router.get('/hub/{id}', response_model=Union[EventSubscription, Error400, Error401, Error403,Error404,  Error500, Error501],
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

async def retrieves_a_hub_by_id(
    response: Response,
    id: str = Path(description = "Identifier of the Hub."),
    
    ):
    """
    The Buyer/Client requests detailed information about a single Notification Hub based on the Hub Identifier.
    """
    add_headers(response)
    try:
        return get_performance_monitoring_hub_by_id(id)
    except Exception as err:
        return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 


