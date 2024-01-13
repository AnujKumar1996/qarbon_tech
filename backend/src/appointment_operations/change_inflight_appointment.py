import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
from src.schemas.sonata_schemas.appointment_schemas import Appointment
from src.common.exceptions import raise_exception
from src.common.validate_datetime import validate_datetime
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime, validate_user_enddatetime, checking_relatedcontactinfo

def change_inflight_appointment(order, id, buyerId, sellerId):
    
    try:
        order_data = order.model_dump(by_alias=True)

        if order_data.get('attachment') is not None or order_data.get('note') is not None or order_data.get('relatedPlace') is not None or order_data.get('relatedContactInformation') is not None or order_data.get('validFor') is not None:
            
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
                    appointment_json_data = json.load(json_file)

            except json.JSONDecodeError as e:
                return raise_exception(status_msg_code=404, 
                                        message="Record not found", 
                                        reason="Record not found", 
                                        reference_error=None, 
                                        message_code="notFound", 
                                        property_path=None)        
            all_keys = appointment_json_data.keys()  

            if id in all_keys and appointment_json_data.get(id).get('id') == id:
                
                appointment_json_data_of_particular_id = appointment_json_data.get(id)
                
                if buyerId != "" and buyerId != appointment_json_data_of_particular_id.get("buyerId"): 
                            
                    status_msg_code = 404
                    message = f"Invalid buyerId '{buyerId}'"
                    reason = "Requested buyerId not found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                if sellerId != "" and  sellerId != appointment_json_data_of_particular_id.get("sellerId"): 

                    status_msg_code = 404
                    message = f"Invalid sellerId '{sellerId}'"
                    reason = "Requested sellerId not Found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                if appointment_json_data_of_particular_id.get("status") != "confirmed":
                    
                    status_msg_code = 422
                    message = "Appointment status is not confirmed."
                    reason = "The appointment update requires the status to be confirmed"
                    reference_error = None
                    message_code = "missingProperty"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                if 'relatedContactInformation' in order_data and order_data['relatedContactInformation'] is not None:
                    
                    is_valid=checking_relatedcontactinfo(order_data, appointment_json_data_of_particular_id)
                    
                    if not is_valid:
                       
                        status_msg_code = 422
                        message = "Modifying relatedContactInformation is not allowed."
                        reason = "The Buyer must not change the relatedContactInformation attribute."
                        reference_error = None
                        message_code = "missingProperty"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                attachment_creationdate=None
                if order_data['attachment'] is not None:
                    for item in order_data['attachment']:
                        attachment_creationdate=item.get('creationDate')
                            
                if order_data['validFor'] is not None:
                    
                    appoint_startdatetime=order_data.get('validFor',  {}).get("startDateTime")
                    appoint_enddatetime=order_data.get('validFor',  {}).get("endDateTime")
                    
                    date_tuple=(appoint_startdatetime,appoint_enddatetime,attachment_creationdate)
                    for date_time in date_tuple:
                        if date_time is not None:
                            isvalid_format = validate_datetime(str(date_time))
                            if isvalid_format:
                                return isvalid_format
                        
                    
                    is_start_datetime_valid=validate_user_startdatetime(str(appoint_startdatetime))

                    is_end_datetime_valid=validate_user_enddatetime(str(appoint_startdatetime),str(appoint_enddatetime))  
                    
                    if not is_start_datetime_valid:

                        return raise_exception(status_msg_code=422, 
                                            message="'start datetime' should be greater than 'current_datetime'",
                                            reason="Invalid 'start datetime'", 
                                            reference_error=None, 
                                            message_code="invalidValue", 
                                            property_path=None) 


                    if not is_end_datetime_valid:

                        return raise_exception(status_msg_code=422, 
                                            message="'end datetime' should be greater than 'start datetime'",
                                            reason="Invalid 'end datetime'", 
                                            reference_error=None, 
                                            message_code="invalidValue", 
                                            property_path=None) 
                    
                        
                    appointment_json_data_of_particular_id['validFor']= order_data.get("validFor")
                
                if order_data['relatedPlace'] is not None:
                    appointment_json_data_of_particular_id['relatedPlace']= order_data.get("relatedPlace")
                    
                if order_data['note'] is not None:  
                            
                    json_res_note_data = appointment_json_data_of_particular_id['note']
                    json_res_note_data.extend(order_data['note'])
                    appointment_json_data_of_particular_id['note'] = json_res_note_data
                
                if order_data['attachment'] is not None: 
                    
                    if appointment_json_data_of_particular_id.get('attachment') is not None:
                        json_res_attachment_data = appointment_json_data_of_particular_id['attachment']
                        json_res_attachment_data.extend(order_data['attachment'])
                        appointment_json_data_of_particular_id['attachment'] = json_res_attachment_data
                    else:
                      appointment_json_data_of_particular_id['attachment'] = order_data['attachment']  
                        
                response_data = jsonable_encoder(Appointment(**appointment_json_data_of_particular_id))
                create_response_json(id, response_data, file_name)
                    
                return JSONResponse(status_code=status.HTTP_200_OK,
                                                    content=response_data,
                                                    media_type="application/json;charset=utf-8"
                                                    )
                
            else:
                
                return raise_exception(status_msg_code=404,
                                    message=f"Id not found '{id}'", 
                                    reason="Id not found",
                                    reference_error=None,
                                    message_code="notFound",
                                    property_path=None)    
    
        else:
            status_msg_code = 422
            message = "At least one of the following attributes is required: 'attachment', 'note', 'relatedContactInformation', 'validFor'."
            reason="Required attributes are missing."
            reference_error = None
            message_code = "missingProperty"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
      
    except Exception as err:
            return raise_exception(status_msg_code=500,
                                   message= str(err), 
                                   reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                   reference_error=None, 
                                   message_code="internalError", 
                                   property_path=None) 
        