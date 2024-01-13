from fastapi import (APIRouter, Response, 
                     status)
from pathlib import Path
import json
from src.common.json_read import common_schema
from src.common.exceptions import raise_exception

from src.schemas.interlude_schemas.notification_schema import PerformanceReportEvent

router = APIRouter(
    prefix="/v1/MEF/lsoInterlude/listener/performanceNotification"
)

@router.post("/performanceReportCreateEvent",
            tags=["performanceNotification Listeners"],
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
            responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        422: common_schema["response_422"],
        500: common_schema["response_500"]
    })
async def Performance_Report_Create_Notification_event(info:PerformanceReportEvent):
    '''
    Client listener for receiving the performanceReportCreateEvent notification
    '''
    
    try:
        cwd = Path(__file__).parents[1]
        response_file="interlude_performanceprofile_response.json"
        fileName = cwd / "responses" / "interlude_performancereport_response.json"
        
        if not fileName.exists():
            status_msg_code = 404
            message = f"File not found: {response_file}"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(fileName, "r") as json_file:
                json_content = json_file.read()
                
            data_json = json.loads(json_content)   
                
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (empty or invalid JSON)
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
 
        if not info.eventId:
            status_msg_code = 422
            message = f"Invalid eventId '{info.eventId}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "eventId"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        if not info.event.id:
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "event.id"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            
        list_of_keys = data_json.keys()
        
        if info.event.id not in list_of_keys:
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "event.id"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        else:   
            jsonresult = data_json[info.event.id] 
            
            if info.event.href != "":
                list_of_keys = data_json.keys()
                href_val = jsonresult["href"]
                if href_val != info.event.href:
                    status_msg_code = 422
                    message = f"Invalid href '{info.event.href}'"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = "event.href"
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                
            current_state = jsonresult.get("state")
            previous_state = jsonresult.get("previoustate")

            if current_state != previous_state:
                jsonresult["previoustate"] = current_state
                with open(fileName, "w") as updated_file:
                    json.dump(data_json, updated_file, indent=4)
                
                if current_state == 'acknowledged' or current_state=='completed' or current_state == 'in-progress':
                    #Successful response
                    return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                elif current_state == 'rejected':
                    #Condition to raise exception for timeout error(Request Time-out)
                    status_msg_code = 422
                    message = "The state remains unchanged"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "otherIssue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            else:
                status_msg_code = 422
                message = "The state remains unchanged"
                reason = "Validation error"
                reference_error = None
                message_code = "otherIssue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                   
                    
            
        
        