import json
from fastapi import status ,Response
from pathlib import Path
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json
from datetime import datetime
def reopen_troubleticket_by_id(order, id, buyerId, sellerId):
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
        
        if troubleticket_item_data.get("status") != "reopened" :
            
            troubleticket_item_data["status"]="reopened"
            new_note = {
                "author": "closureRejection",
                "date": datetime.utcnow().isoformat(),
                "id": "004",
                "source": "buyer",
                "text": f"{order.reason}"
            }
            if troubleticket_item_data.get('note') is not None:  
                    
                json_res_note_data = troubleticket_item_data['note']
                json_res_note_data.append(new_note)
                troubleticket_item_data['note'] = json_res_note_data
            else:
                troubleticket_item_data['note'] = new_note 
                
            
            create_response_json(id, troubleticket_item_data, file_name)
            
            return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
        else:
            status_msg_code = 422
            message = "The trouble ticket has already been set to the 'reopened' status."
            reason = "The troubleTicket is remains reopened"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
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