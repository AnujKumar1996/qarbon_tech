from pathlib import Path
import json
from fastapi import status
from src.schemas.sonata_schemas.appointment_schemas import Appointment_Find
from src.common.validate_datetime import validate_datetime_format
from src.common.exceptions import raise_exception
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.validation.sonata.validate_appointment_by_id import validate_appointment_by_id

def retrieve_appointment_list(workOrderId,
                               appointment_status,
                               validFor_gt,
                               validFor_lt,
                               geographicalSiteId,
                               geographicalAddressId,
                               buyerId, sellerId, offset, limit):
   
    """
    This function retrieves a appointment by List.
    """
    
    try:
        
        date_tuple = (validFor_gt, validFor_lt)
        for date_data in date_tuple:
                if date_data is not None:
                    isvalid_format = validate_datetime_format(date_data)
                    if isvalid_format:
                        return isvalid_format
        
        if offset is not None and offset < 0:
                status_msg_code = 400
                message = "'offset' cannot be negative"
                reason = "Invalid offset value"
                reference_error = None
                message_code = "invalidQuery"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if limit is not None and limit < 0:
            status_msg_code = 400
            message = "'limit' cannot be negative"
            reason = "Invalid limit value"
            reference_error = None
            message_code = "invalidQuery"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if offset is None: offset = 0
        if limit is None: limit = 10      
                    
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
        
        
        extracted_data = []
        for _, category_info in json_data.items():
            json_workorderId = category_info.get("workOrder").get('id')
            json_geographicalAddressId = category_info.get("geographicalAddressId")
            json_geographicalSiteId = category_info.get("geographicalSiteId")
            json_status = category_info.get("status")
            json_startDateTime = category_info.get("validFor").get("startDateTime")
            json_endDateTime=category_info.get("validFor").get("endDateTime")
            json_buyerId = category_info.get("buyerId")
            json_sellerId = category_info.get("sellerId")
        
            if ((workOrderId == "" or workOrderId == json_workorderId) and
                (appointment_status == ""  or appointment_status == json_status) and
                (geographicalSiteId == ""  or geographicalSiteId == json_geographicalSiteId) and
                (geographicalAddressId == ""  or geographicalAddressId == json_geographicalAddressId) and
                (validFor_gt is None  or (validFor_gt and validFor_gt <= json_startDateTime)) and
                (validFor_lt is None  or (validFor_lt and validFor_lt >= json_endDateTime)) and
                (buyerId == ""  or buyerId == json_buyerId) and
                (sellerId == ""  or sellerId == json_sellerId)
                ):
                extracted_info = {
                    "id": category_info.get("id"),
                    "href": category_info.get("href"),
                    "workOrder": category_info.get("workOrder"),
                    "status": category_info.get("status"),
                    "validFor": category_info.get("validFor"),
                    "relatedPlace": category_info.get("relatedPlace"),
                }
                extracted_data.append(extracted_info)
        limited_responses = extracted_data[offset : offset + limit]   
    
        if not limited_responses or not extracted_data:
                status_msg_code = 404
                message = "No matching result found for the given criteria."
                reason = "Record not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        limited_responses_schema = [Appointment_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        
        validation = validate_appointment_by_id(json_data,workOrderId, appointment_status)

        if validation is True:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8")
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
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
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
  