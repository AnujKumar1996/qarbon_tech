from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.product_offering_qualification_schema import Event
from src.product_offering_qualification_operations.poq_state_change_event_notification import product_offering_qualification_state_change_Event_notification
from src.product_offering_qualification_operations.poq_create_event_notification import product_offering_qualification_createEvent_notification
from src.product_offering_qualification_operations.poq_item_state_change_notification import poq_item_state_change


from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOfferingQualificationNotification/listener",
    tags=["Product Offering Qualification Notification"]
)
      
@router.post("/poqStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    500: common_schema["response_500"]
    
})

def product_offering_qualification_change_notification_endpoint(info:Event):
    """
    This endpoint is used to receive notifications on POQ state change
    """
    try:
       return product_offering_qualification_state_change_Event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

@router.post("/poqCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    500: common_schema["response_500"]
    
})

def product_offering_qualification_creation_notification_endpoint(info: Event):
    """
    This endpoint is used to receive notifications on POQ creation
    """
    try:
       return product_offering_qualification_createEvent_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

@router.post("/poqItemStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    500: common_schema["response_500"]
    
})

def poq_item_state_change_notification_endpoint(info: Event):
    """
    This endpoint is used to receive notifications on Poq Item state change
    """
    try:
       return poq_item_state_change(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)