import json
from fastapi import status ,Response
from pathlib import Path
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json


def cancel_troubleticket_by_id(id, buyerId, sellerId):
    try:
        current_directory = Path(__file__).parents[1]
        response_file = 'trouble_ticket.json'
        file_name = current_directory / 'responses/trouble_ticket.json'

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found '{response_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)
        except json.JSONDecodeError:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        troubleticket_items = json_data.keys()
        if id in troubleticket_items:
            troubleticket_item_data = json_data[id]   
            if troubleticket_item_data["id"] == id:
                if buyerId != "" and troubleticket_item_data.get("buyerId") != buyerId: 
                    status_msg_code = 404
                    message = f"Invalid buyerId '{buyerId}'"                        
                    reason = "Requested buyerId not found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                if sellerId != "" and troubleticket_item_data.get("sellerId") != sellerId: 
                    status_msg_code = 404
                    message = f"Invalid sellerId '{sellerId}'"
                    reason = "Requested sellerId not Found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            else:    
                status_msg_code = 404
                message = f"Id not found '{id}'"
                reason = "Requested id not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if troubleticket_item_data.get("status")=="resolved" or troubleticket_item_data.get("status")=="closed" or troubleticket_item_data.get("status")=="reopened" or troubleticket_item_data.get("status")=="assessingCancellation" or troubleticket_item_data.get("status")=="cancelled":
            
            status_msg_code = 422
            message = "The buyer cannot cancel the TroubleTicket in these following status: 'resolved', 'closed', 'reopened', 'assessingCancellation', 'cancelled'"
            reason = "The TroubleTicket cannot be canceled by the buyer when it is in the following statuses: 'resolved', 'closed', 'reopened', 'assessingCancellation', 'cancelled'"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
        if troubleticket_item_data.get("status")=="acknowledged" or troubleticket_item_data.get("status")=="inProgress" or troubleticket_item_data.get("status")=="pending" :
            
            troubleticket_item_data["status"]="assessingCancellation"
            create_response_json(id, troubleticket_item_data, file_name)
            
            return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, 
                               message, reason, 
                               reference_error, 
                               message_code, 
                               property_path)