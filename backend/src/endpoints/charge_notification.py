import json
from pathlib import Path
from src.common.exceptions import raise_exception
from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.common_schemas import ChargeEvent
from src.common.exceptions import raise_exception
from src.notification_operations.charge_create_event_notification import charge_create_event
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime
from src.common.validate_datetime import validate_datetime 

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOrderingManagement/listener",
    tags=["productOrder Notification Listeners"]
)

@router.post("/chargeStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })

def charge_state_change_notification_endpoint(info:ChargeEvent):

    """
    This endpoint is used to receive notifications on Charge Create Event
    """
    try:
        cwd = Path(__file__).parents[1]
        charge_file="charge_response.json"
        charge_response_filename = cwd / "responses" / charge_file
      
        if not charge_response_filename.exists():
            status_msg_code = 404
            message = f"File not found: {charge_file}"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:        
            with open(charge_response_filename, "r") as json_file:
                charge_json = json.load(json_file)
                
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "chargeStateChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'chargeStateChangeEvent'"
            reason = "The requested eventType is invalid"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if not isvalid_format:
            return isvalid_format
        
        validate_event_time = validate_user_startdatetime(event_time)
        if validate_event_time:
            status_msg_code = 422
            message = "The provided eventTime is invalid"
            reason = "The eventTime should be a valid current timestamp"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
     
        list_of_keys = charge_json.keys()  
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            charge_data=charge_json[info.event.id]
            
            if info.event.sellerId !=  "" and charge_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            if info.event.buyerId !=  "" and charge_data["buyerId"]!=info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
                    
            if info.event.href !=  "" and charge_data["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
           
            current_state = charge_data.get("state")
            previous_state = charge_data.get("previoustate")
            
            if current_state != previous_state:
                charge_data["previoustate"] = current_state
                 
                with open(charge_response_filename, "w") as updated_file:
                    json.dump(charge_json, updated_file, indent=4)
                    #Successful response
                    return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "The state remains unchanged"
                reason = "The cancellation of the product is still in the same state"
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
                                                            

@router.post("/chargeCreateEvent",status_code=status.HTTP_204_NO_CONTENT ,response_class=Response,
            responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })
def charge_create_notification_endpoint(info:ChargeEvent):

    
    """
    This endpoint is used to receive notifications on Charge Create Event
    """ 
    try:
            return charge_create_event(info)
    except Exception as err:
            return raise_exception(500, str(err), "The server encountered an unexpected condition that prevented it from fulfilling the request", None, "internalError", None) 

                           
@router.post("/chargeTimeoutEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })

def charge_state_change_notification_endpoint(info:ChargeEvent):

    try:    
        cwd = Path(__file__).parents[1]

        charge_file="charge_response.json"
        charge_response_filename = cwd / "responses" / charge_file
            
        if not charge_response_filename.exists():
            status_msg_code = 404
            message = f"File not found '{charge_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:        
            with open(charge_response_filename, "r") as json_file:
                charge_json = json.load(json_file)
                
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "chargeTimeoutEvent":
            status_msg_code = 422
            message = "The eventType must be 'chargeTimeoutEvent'"
            reason = "The requested eventType is invalid"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if not isvalid_format:
            return isvalid_format
        
        validate_event_time = validate_user_startdatetime(event_time)
        if validate_event_time:
            status_msg_code = 422
            message = "The provided event time is invalid"
            reason = "The event time should be a valid current timestamp"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
     
        list_of_keys = charge_json.keys()  
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            charge_data=charge_json[info.event.id]
            
            if info.event.sellerId != "" and charge_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            if info.event.buyerId != "" and charge_data["buyerId"]!=info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            if info.event.href != "" and charge_data["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            current_state = charge_data.get("state")
            previous_state = charge_data.get("previoustate")
            
            if current_state == previous_state:
                status_msg_code = 422
                message = "The state remains unchanged"
                reason = "The state remains the same"
                reference_error = None
                message_code = "otherIssue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            if current_state == "timeout":
                charge_data["previoustate"] = current_state
                    
                with open(charge_response_filename, "w") as updated_file:
                    json.dump(charge_json, updated_file, indent=4)
                    #Successful response
                    return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
               
            else:
                status_msg_code = 422
                message = "The current state is not in 'timeout' state"
                reason = "The state is not currently in a 'timeout' state"
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