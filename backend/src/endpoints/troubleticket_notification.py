from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.trouble_ticket_schema import TroubleTicketEvent
from src.trouble_ticket_operations.notification_troubleticket_attribute_value_change_event import troubleticket_attribute_value_change_event
from src.trouble_ticket_operations.notification_troubleticket_state_change_event import troubleticket_state_change_event
from src.trouble_ticket_operations.notification_troubleticket_resolved_event import troubleticket_resolved_event
from src.trouble_ticket_operations.notification_troubleticket_information_requiredevent import troubleticket_information_requiredevent


router = APIRouter(
    prefix="/v1/MEF/lsoSonata/troubleTicketNotification",
    tags=["Trouble Ticket and Incident Notification"]
)
      
@router.post("/listener/troubleTicketAttributeValueChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_troubleticketattributevaluechangeevent(info:TroubleTicketEvent):
    """
    Client listener for receiving the notification TroubleTicketAttributeValueChangeEvent
    """
    try:
       return troubleticket_attribute_value_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/listener/troubleTicketStatusChangeEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )

def client_listener_for_entity_troubleticketstatuschangeevent(info:TroubleTicketEvent):
    """
    Client listener for receiving the notification TroubleTicketStatusChangeEvent
    """
    try:
        return troubleticket_state_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/listener/troubleTicketResolvedEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )

def client_listener_for_entity_troubleticketresolvedevent(info:TroubleTicketEvent):
    """
    Client listener for receiving the notification TroubleTicketResolvedEvent 
    """
    try:
        return troubleticket_resolved_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/listener/troubleTicketInformationRequiredEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )

def client_listener_for_entity_troubleticketinformationrequiredevent(info:TroubleTicketEvent):
    """
    Client listener for receiving the notification TroubleTicketInformationRequiredEvent
    """
    try:
        return troubleticket_information_requiredevent(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

