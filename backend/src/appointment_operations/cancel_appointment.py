import json
from pathlib import Path
from fastapi import status, Response
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json

def cancel_appointment(id, buyerId, sellerId):
    
    """
    This operation sends a cancellation request.
    """
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "appointment.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                    message=f"File not found '{response_file}'",
                                    reason="File not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)        
       
        workorder_response_file = "workorder.json"
        workorder_file_name = current_directory / 'responses'/workorder_response_file
            
        if not workorder_file_name.exists():
            
                return raise_exception(status_msg_code=404,
                                message=f"File not found '{response_file}'",
                                reason="File not found", 
                                reference_error=None, 
                                message_code="notFound", 
                                property_path=None)
        try:
            with open(workorder_file_name,'r') as json_file:
                workorder_json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)    
            
       
        all_keys = json_data.keys()  
        
        if id in all_keys and json_data.get(id).get('id') == id:
           
            appointment_jsondata = json_data.get(id)
            workorderId=appointment_jsondata.get('workOrder').get("id")
            
            
            if buyerId != "" and buyerId != appointment_jsondata.get("buyerId"): 
                        
                status_msg_code = 404
                message = f"Invalid buyerId '{buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if sellerId != "" and  sellerId != appointment_jsondata.get("sellerId"): 

                status_msg_code = 404
                message = f"Invalid sellerId '{sellerId}'"
                reason = "Requested sellerId not Found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if appointment_jsondata.get("status") != "confirmed":
                status_msg_code = 422
                message = "Appointment status is not confirmed."
                reason = "Invalid Appointment Status"
                reference_error = None
                message_code = "missingProperty"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


            work_order_info = workorder_json_data[workorderId]
            
            if work_order_info.get('state') != "planned":
                status_msg_code = 422
                message = "Invalid Workorder State."
                reason = "Workorder must be in 'planned' state for Seller Response."
                reference_error = None
                message_code = "missingProperty"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


            work_order_info['appointmentRequired'] = True
            work_order_info['state'] = 'open'
            appointment_jsondata['status'] ="cancelled"
            
            
            create_response_json(workorderId, work_order_info, workorder_file_name)  
            create_response_json(id, appointment_jsondata, file_name)         
            return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                     
        else:
            return raise_exception(status_msg_code=404,
                                   message=f"Id not found '{id}'", 
                                   reason="'Id' not found",
                                   reference_error=None,
                                   message_code="notFound",
                                   property_path=None)
            
    except Exception as err:
            return raise_exception(status_msg_code=500,
                                   message= str(err), 
                                   reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                   reference_error=None, 
                                   message_code="internalError", 
                                   property_path=None) 
