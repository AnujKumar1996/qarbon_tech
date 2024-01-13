import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json
from src.common.validate_datetime import validate_datetime 
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime

def troubleticket_resolved_event(info):

    try:
        # Get the parent directory of the current file
        cwd = Path(__file__).parents[1]
        
         # Define the file paths
        troubleticket_file = "trouble_ticket.json"
        troubleticket_response_filename = cwd / "responses" / troubleticket_file 
        
        # Check if the file exists
        if not troubleticket_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{troubleticket_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            # Load JSON data from the file
            with open(troubleticket_response_filename, "r") as json_file:
                data_json = json.load(json_file)
        
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        # Check if eventType is 'troubleTicketResolvedEvent'
        if info.eventType != "troubleTicketResolvedEvent":
            status_msg_code = 422
            message = "The eventType must be 'troubleTicketResolvedEvent'"
            reason = "Invalid requested eventType"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

         # Validate eventTime format
        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if isvalid_format:
            return isvalid_format
        
        # Validate eventTime against user-defined rules
        validate_event_time = validate_user_startdatetime(event_time)
        if not validate_event_time:
            status_msg_code = 422
            message = "The provided eventTime is invalid"
            reason = "The eventTime should be a valid current timestamp"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        list_of_keys = data_json.keys()  
        
        # Check if event.id is in the list of keys in the JSON data
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            troubleticket_data=data_json[info.event.id]
            
             # Check if sellerId, buyerId, and href match expected values
             
            if info.event.sellerId != "" and troubleticket_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                      
            if info.event.buyerId != "" and troubleticket_data["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and troubleticket_data["href"] != info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            current_state = troubleticket_data.get("status")
            
            if current_state == "resolved":
                # If the trouble ticket is already resolved
                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = f"The trouble ticket is currently in the '{current_state}' state."
                reason = "The trouble ticket remains unresolved."
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


                