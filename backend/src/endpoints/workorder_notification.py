from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.work_order_schemas import WorkOrderEventWorkOrderEvent
from src.workorder_operations.workorder_create_event_notification import workorder_create_event
from src.workorder_operations.workorder_statechange_event_notification import workorder_state_change_event
from src.workorder_operations.workorder_appointment_required_event_notification import workorder_appointment_required_event


from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/workOrderNotification/listener",
    tags=["WorkOrder Management Notification"]
)
      
@router.post("/workOrderCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    422: common_schema["response_422"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_workorder_create_event(info:WorkOrderEventWorkOrderEvent):
    """
    Client listener for receiving the notification WorkOrder Create Event
    """
    try:
       return workorder_create_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    
    
@router.post("/workOrderStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    422: common_schema["response_422"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_workorderstatechangeevent(info:WorkOrderEventWorkOrderEvent):
    """
    Client listener for receiving the workOrderStateChangeEvent notification
    """
    try:
       return workorder_state_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    

@router.post("/workOrderAppointmentRequiredEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    422: common_schema["response_422"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_workorderappointmentrequiredevent(info:WorkOrderEventWorkOrderEvent):
    """
    Client listener for receiving the workOrderAppointmentRequiredEvent notification
    """
    try:
       return workorder_appointment_required_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    