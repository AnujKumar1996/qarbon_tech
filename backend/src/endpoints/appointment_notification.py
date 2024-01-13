from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.appointment_schemas import AppointmentEvent
from src.appointment_operations.appointment_attribute_value_change_notification import appointment_attribute_value_change_event
from src.appointment_operations.appointment_state_change_notification import appointment_state_value_change_event
from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/appointmentNotification/appointment/listener",
    tags=["Appointment Management Notification"]
)

@router.post("/appointmentAttributeValueChangeEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )
def client_listener_for_entity_appointmentattributevaluechangeevent(info:AppointmentEvent):
    """
    Client listener for receiving the appointmentAttributeValueChangeEvent notification
    """
    try:
        return appointment_attribute_value_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

@router.post("/appointmentStatusChangeEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )

def client_listener_for_entity_appointmentstatuschangeevent(info:AppointmentEvent):
    """
    Client listener for receiving the appointmentStatusChangeEvent notification
    """
    try:
        return appointment_state_value_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
