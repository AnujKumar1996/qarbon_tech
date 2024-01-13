import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.validate_datetime import validate_datetime ,validate_datetime_format
from src.schemas.sonata_schemas.appointment_schemas import SearchTimeSlot
from src.common.create_jsonfile import create_response_json
from src.validation.sonata.validate_searchtimeslot import validate_searchtimeslot, validate_endDateTime, validate_startDateTime, validate_user_startDateTime, validate_user_endDateTime
from src.common.exceptions import raise_exception

def create_a_timeslot(order, buyerId, sellerId):
    
    """
    This function register for timeslot at the seller.
    """

    order_data = order.model_dump(by_alias=True)
    try:
            
        current_directory = Path(__file__).parents[1]
        response_file = "appointment_searchtimeslot.json"
        file_name = current_directory / 'responses'/response_file
        
        
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
            
    
        buyer_requestedTimeSlot = order_data.get('requestedTimeSlot')
        
        for item in buyer_requestedTimeSlot:
            
            validFor = item.get('validFor')  
            endDateTime = str(validFor.get("endDateTime") )
            startDateTime = str(validFor.get("startDateTime"))
        
        date_tuple = (endDateTime,startDateTime)
        
        for date_data in date_tuple:
                if date_data is not None:
                    isvalid_format = validate_datetime(date_data)
                    if isvalid_format:
                        return isvalid_format
    
                            
        is_buyer_start_datetime_valid=validate_user_startDateTime(order_data)

        is_buyer_end_datetime_valid=validate_user_endDateTime(order_data)

        if not is_buyer_start_datetime_valid:

            return raise_exception(status_msg_code=422, 
                                message="Request 'start datetime' should be greater than 'current_datetime'",
                                reason="Invalid 'start datetime'", 
                                reference_error=None, 
                                message_code="invalidValue", 
                                property_path=None) 


        if not is_buyer_end_datetime_valid:

            return raise_exception(status_msg_code=422, 
                                message="Request 'end datetime' should be greater than 'start datetime'",
                                reason="Invalid 'end datetime'", 
                                reference_error=None, 
                                message_code="invalidValue", 
                                property_path=None) 

        workOrderId=order_data.get('workOrder').get("id")  
        
        all_keys = workorder_json_data.keys() 
        
        if workOrderId in all_keys and workorder_json_data.get(workOrderId).get('id') == workOrderId: 
            
            workorder_data = workorder_json_data.get(workOrderId)
            
            if workorder_data.get("appointmentRequired") ==True:
                
                payload_file_name = current_directory / 'common/sonata_payloads.json'
                with open(payload_file_name, "r") as json_file:
                    json_payload = json.load(json_file)
                    
                order_data["id"] = json_payload.get("searchTimeSlot_201", {}).get("id")
                order_data["availableTimeSlot"] = json_payload.get("searchTimeSlot_201", {}).get("availableTimeSlot")

                response_data = jsonable_encoder(SearchTimeSlot(**order_data))
                
                seller_availableTimeSlot=response_data.get('availableTimeSlot')
                
                for item in seller_availableTimeSlot:
                    
                    validFor=item.get('validFor')  
                    seler_startDateTime=validFor.get("startDateTime")
                    seller_endDateTime=validFor.get("endDateTime")
            
                date_tuple = (seler_startDateTime,seller_endDateTime)
                for date_data in date_tuple:
                        if date_data is not None:
                            isvalid_format = validate_datetime_format(date_data)
                            if isvalid_format:
                                return isvalid_format
                    

                is_seller_datetime_valid=validate_startDateTime(response_data)

                is_seller_datetime_valid=validate_endDateTime(response_data)

                is_validated=validate_searchtimeslot(order_data, response_data)

                if not is_seller_datetime_valid:

                    return raise_exception(status_msg_code=422, 
                                        message="Response 'start datetime' should be greater than 'current_datetime'",
                                        reason="validation Error", 
                                        reference_error=None, 
                                        message_code="invalidValue", 
                                        property_path=None) 


                if not is_seller_datetime_valid:

                    return raise_exception(status_msg_code=422, 
                                        message="Response 'end datetime' should be greater than 'start datetime'",
                                        reason="validation Error", 
                                        reference_error=None, 
                                        message_code="invalidValue", 
                                        property_path=None) 



                if not is_validated:
                    return raise_exception(status_msg_code=422, 
                                        message="Request and Response data are mismatching",
                                        reason="validation Error", 
                                        reference_error=None, 
                                        message_code="invalidValue", 
                                        property_path=None)

                json_response = response_data.copy()
                json_response["buyerId"] = buyerId
                json_response["sellerId"] = sellerId

                create_response_json(order_data["id"], json_response,file_name)
                return JSONResponse(status_code=status.HTTP_201_CREATED,
                                                content=response_data,
                                                media_type="application/json;charset=utf-8"
                                                )
            
            else:
                return raise_exception(status_msg_code=422, 
                                    message="Appointment denied by seller",
                                    reason="The seller has no appointment request for this workOrderId", 
                                    reference_error=None, 
                                    message_code="invalidValue", 
                                    property_path=None) 
                    
        else:
            
            return raise_exception(status_msg_code=422, 
                                    message=f"Invalid workOrderId '{workOrderId}'",
                                    reason="validation Error", 
                                    reference_error=None, 
                                    message_code="invalidValue", 
                                    property_path=None) 
        
    except Exception as err:
            return raise_exception(status_msg_code=500,
                                   message= str(err), 
                                   reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                   reference_error=None, 
                                   message_code="internalError", 
                                   property_path=None) 
