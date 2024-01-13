import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json
from src.common.validate_datetime import validate_datetime 
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime


def troubleticket_attribute_value_change_event(info):

    try:
        cwd = Path(__file__).parents[1]
        troubleticket_file = "trouble_ticket.json"
        troubleticket_response_filename = cwd / "responses" / troubleticket_file 
        
        if not troubleticket_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{troubleticket_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
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

        if info.eventType != "troubleTicketAttributeValueChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'troubleTicketAttributeValueChangeEvent'"
            reason = "Requested eventType is invalid"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if isvalid_format:
            return isvalid_format
        
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
        
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested Id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            troubleticket_data=data_json[info.event.id]
            
            if info.event.sellerId != "" and troubleticket_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found."
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
            
            current_sellerSeverity = troubleticket_data.get("sellerSeverity")
            previous_sellerSeverity = troubleticket_data.get("previousSellerSeverity")
            
            current_sellerPriority = troubleticket_data.get("sellerPriority")
            previous_sellerPriority = troubleticket_data.get("previousSellerPriority")
            
            current_note = troubleticket_data.get("note")
            previous_note = troubleticket_data.get("previousNote")
            
            current_expectedResolutionDate = troubleticket_data.get("expectedResolutionDate")
            previous_expectedResolutionDate = troubleticket_data.get("previousExpectedResolutionDate")
            
            current_attachment = troubleticket_data.get("attachment")
            previous_attachment = troubleticket_data.get("previousAttachment")
            
            current_relatedContactInformation = troubleticket_data.get("relatedContactInformation")
            previous_relatedContactInformation = troubleticket_data.get("previousRelatedContactInformation")
            
            current_relatedIssue = troubleticket_data.get("relatedIssue")
            previous_relatedIssue = troubleticket_data.get("previousRelatedIssue")
            
            current_workOrder = troubleticket_data.get("workOrder")
            previous_workOrder = troubleticket_data.get("previousWorkOrder")
            
            attributes_changed = False
            
            if current_sellerSeverity != previous_sellerSeverity:
                troubleticket_data["previousSellerSeverity"] = current_sellerSeverity
                attributes_changed = True
               
            if current_sellerPriority != previous_sellerPriority:
                troubleticket_data["previousSellerPriority"] = current_sellerPriority
                attributes_changed = True
           
            if current_note != previous_note:
                troubleticket_data["previousNote"] = current_note
                attributes_changed = True
            
            if current_expectedResolutionDate != previous_expectedResolutionDate:
                troubleticket_data["previousExpectedResolutionDate"] = current_expectedResolutionDate
                attributes_changed = True
                
            if current_attachment != previous_attachment:
                troubleticket_data["previousAttachment"] = current_attachment
                attributes_changed = True
                
            if current_relatedContactInformation != previous_relatedContactInformation:
                troubleticket_data["previousRelatedContactInformation"] = current_relatedContactInformation
                attributes_changed = True
                
            if current_relatedIssue != previous_relatedIssue:
                troubleticket_data["previousRelatedIssue"] = current_relatedIssue
                attributes_changed = True
                
            if current_workOrder != previous_workOrder:
                troubleticket_data["previousWorkOrder"] = current_workOrder
                attributes_changed = True
                
            
            if attributes_changed:
               create_response_json(info.event.id, troubleticket_data, troubleticket_response_filename)
               return Response(status_code = status.HTTP_204_NO_CONTENT,media_type = "application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "Trouble ticket attributes remain unchanged."
                reason = "No attribute changes detected in the trouble ticket"
                reference_error = None
                message_code = "otherIssue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request."
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


                