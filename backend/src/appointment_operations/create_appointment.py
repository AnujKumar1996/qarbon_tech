import json
from datetime import datetime
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.validate_datetime import validate_datetime
from src.schemas.sonata_schemas.appointment_schemas import Appointment
from src.common.create_jsonfile import create_response_json
from src.validation.sonata.validate_create_appointment import validate_create_appointment ,validate_user_startdatetime, validate_user_enddatetime, convert_to_utc_iso_range
from src.common.exceptions import raise_exception


def create_appointment(order, buyerId, sellerId):

    """
    This function creates appointment  .
    """
    
    try:
        order_data = order.model_dump(by_alias=True)
        
        attachment_creationdate = None
        if order_data['attachment'] is not None:
            for item in order_data['attachment']:
                attachment_creationdate=item.get('creationDate')
                
        buyer_startdatetime=order_data.get('validFor', {}).get("startDateTime")
        buyer_enddatetime=order_data.get('validFor', {}).get("endDateTime")
        
        date_tuple = (buyer_startdatetime,buyer_enddatetime,attachment_creationdate)
        for date_time in date_tuple:
                if date_time is not None:
                    isvalid_format = validate_datetime(str(date_time))
                    if isvalid_format:
                        return isvalid_format
        
        for items in order_data.get("relatedContactInformation"):
            if items.get("role") != "buyerAppointmentContact" and items.get("role") != "appointmentPlaceContact":
                status_msg_code = 422
                message = "The Buyer's request MUST specify a relatedContactInformation item with a role set to buyerAppointmentContact or appointmentPlaceContact"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        is_start_datetime_valid=validate_user_startdatetime(str(buyer_startdatetime))

        is_end_datetime_valid=validate_user_enddatetime(str(buyer_startdatetime),str(buyer_enddatetime))  
        
        if not is_start_datetime_valid:

            return raise_exception(status_msg_code=422, 
                                message="Request 'startdatetime' should be greater than 'current_datetime'",
                                reason="Invalid 'startdatetime'", 
                                reference_error=None, 
                                message_code="invalidValue", 
                                property_path=None) 


        if not is_end_datetime_valid:

            return raise_exception(status_msg_code=422, 
                                message="Request 'enddatetime' should be greater than 'startdatetime'",
                                reason="Invalid 'enddatetime'", 
                                reference_error=None, 
                                message_code="invalidValue", 
                                property_path=None) 
    
        current_directory = Path(__file__).parents[1]
        response_file = "appointment.json"
        file_name = current_directory / 'responses'/response_file
        
        workorder_response_file = "workorder.json"
        workorder_file_name = current_directory / 'responses'/workorder_response_file
       
        current_directory = Path(__file__).parents[1]
        response_file = "appointment_searchtimeslot.json"
        serchtimeslot_file_name = current_directory / 'responses'/response_file
        
        if not serchtimeslot_file_name.exists():
            
                return raise_exception(status_msg_code=404,
                                message=f"File not found '{response_file}'",
                                reason="File not found", 
                                reference_error=None, 
                                message_code="notFound", 
                                property_path=None)
        try:
            with open(serchtimeslot_file_name,'r') as json_file:
                serchtimeslot_json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)     
            
        
        if not workorder_file_name.exists():
            
            return raise_exception(status_msg_code=404,
                            message=f"File not found '{response_file}'",
                            reason="File not found", 
                            reference_error=None, 
                            message_code="notFound", 
                            property_path=None)
                
        try:
            with open(workorder_file_name,'r') as json_file:
                workOrder_json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)    
            
        
                
        workOrderId=order_data.get('workOrder').get("id")  
        
        all_keys = workOrder_json_data.keys() 
            
        if workOrderId in all_keys and workOrder_json_data.get(workOrderId).get('id') == workOrderId:  
            
            found = False
            for key, value in serchtimeslot_json_data.items():
                
                timeslot_workorderid=value.get('workOrder', {}).get("id")
                
                if timeslot_workorderid == workOrderId:
                    
                    for item in value.get('availableTimeSlot'):
                        validFor = item.get('validFor')  
                        timeslot_enddatetime = validFor.get("endDateTime") 
                        timeslot_startdatetime = validFor.get("startDateTime")
                        
                        converted_startdatetime, converted_enddatetime = convert_to_utc_iso_range(buyer_startdatetime, buyer_enddatetime)
                       
                        if timeslot_startdatetime == converted_startdatetime  and timeslot_enddatetime == converted_enddatetime:
                            
                            found=True
                           
                
            if found:
                payload_file_name = current_directory / 'common/sonata_payloads.json'
                with open(payload_file_name, "r") as json_file:
                    json_payload = json.load(json_file)
                
                order_data["id"] = json_payload.get("appointment", {}).get("id")
                order_data["href"] = json_payload.get("appointment", {}).get("href")
                order_data["status"] = json_payload.get("appointment", {}).get("status")
                order_data["relatedPlace"] = json_payload.get("appointment", {}).get("relatedPlace")

            
                response_data = jsonable_encoder(Appointment(**order_data))
                
                is_validated=validate_create_appointment(order_data, response_data)
                
                if not is_validated:
                            status_msg_code = 422
                            message = "Request and Response data mismatch."
                            reason = "Validation error"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                                        
                json_response = response_data.copy()
                json_response["buyerId"] = buyerId
                json_response["sellerId"] = sellerId
                json_response["previousStatus"] = order_data["status"]

                create_response_json(order_data["id"], json_response,file_name)
                return JSONResponse(status_code=status.HTTP_201_CREATED,
                                                content=response_data,
                                                media_type="application/json;charset=utf-8"
                                                )
            
            else:
               
                status_msg_code = 422
                message = "The provided timeslot is not available."
                reason = "Invalid timeslot"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
 
        else:
            return raise_exception(status_msg_code=422, 
                                    message=f"Invalid workOrderId '{workOrderId}'",
                                    reason="validation Error", 
                                    reference_error=None, 
                                    message_code="invalidValue", 
                                    property_path=None) 
            
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
