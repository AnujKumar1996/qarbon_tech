from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.customer_bill_management_schemas import CustomerBillEvent
from src.customer_bill_operations.customer_bill_create_event_notification import customer_bill_create_event_notification
from src.customer_bill_operations.customer_bill_state_change_event_notification import customer_bill_state_change_event_notification

router=APIRouter(prefix="/v1/MEF/lsoSonata/customerBillNotification",
                 tags=["Customer Bill Notification Listeners"])

@router.post("/listener/customerBillCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})             
def client_listener_for_customer_bill_create_event(info:CustomerBillEvent):
    
    """
    Client listener for receiving the billCreatedEvent notification
    """
    try:
       return customer_bill_create_event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)



@router.post("/listener/customerBillStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })             
async def client_listener_for_customer_bill_state_change_event(info:CustomerBillEvent):
    
    """
    Client listener for receiving the customerBillStateChangeEvent notification
    """
    try:
       return customer_bill_state_change_event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)






