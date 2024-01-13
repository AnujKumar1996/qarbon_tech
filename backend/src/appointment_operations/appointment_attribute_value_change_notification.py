import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json

def appointment_attribute_value_change_event(info):

    try:
        cwd = Path(__file__).parents[1]
        appointment_file = "appointment.json"
        appointment_response_filename = cwd / "responses" / appointment_file 
        
        if not appointment_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{appointment_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(appointment_response_filename, "r") as json_file:
                data_json = json.load(json_file)
        
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "appointmentAttributeValueChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'appointmentAttributeValueChangeEvent'"
            reason = "Invalid requested eventType"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
        list_of_keys = data_json.keys()  
        
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            appointment_data=data_json[info.event.id]
            
            if info.event.sellerId != "" and appointment_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            if info.event.buyerId != "" and appointment_data["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and appointment_data["href"] != info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            current_attachment = appointment_data.get("attachment")
            previous_attachment = appointment_data.get("previousAttachment")
            
            current_note = appointment_data.get("note")
            previous_note = appointment_data.get("previousNote")
            
            current_relatedcontactinformation = appointment_data.get("relatedContactInformation")
            previous_relatedcontactinformation = appointment_data.get("previousrelatedContactInformation")
          
            attributes_changed = False
            
            if current_attachment != previous_attachment:
                appointment_data["previousAttachment"] = current_attachment
                attributes_changed = True
           
            if current_note != previous_note:
                appointment_data["previousNote"] = current_note
                attributes_changed = True
            
            for item in appointment_data.get("relatedContactInformation"):
                for previousitem in appointment_data.get("previousrelatedContactInformation"):
                    if item.get("role") == "sellerAppointmentContact" and previousitem.get("role") == "sellerAppointmentContact":
                        if item != previousitem:
                            appointment_data["previousrelatedContactInformation"] = current_relatedcontactinformation
                            attributes_changed=True
        
            if attributes_changed:
               create_response_json(info.event.id, appointment_data, appointment_response_filename)
               return Response(status_code = status.HTTP_204_NO_CONTENT,media_type = "application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "Appointment attributes remain unchanged"
                reason = "No modifications were made to the appointment attributes"
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


                