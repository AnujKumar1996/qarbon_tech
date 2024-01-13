import json
from pathlib import Path
from fastapi import status
from src.common.exceptions import raise_exception
from src.common.validate_datetime import validate_datetime_format
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.customer_bill_management_schemas import CustomerBill_Find
from src.validation.sonata.validate_customer_bill_by_list import validate_customer_bill_by_list

def retrive_customer_bill_list(billingAccount_id, billingPeriod_startDateTime_lt, billingPeriod_startDateTime_gt, billingPeriod_endDateTime_lt, billingPeriod_endDateTime_gt,  
                        category, state, offset, limit) :
    
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "customer_bill_management.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                    message=f"File not found {response_file}",
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

        date_tuple = (billingPeriod_startDateTime_lt, billingPeriod_startDateTime_gt, billingPeriod_endDateTime_lt, billingPeriod_endDateTime_gt)
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
        extracted_data = []
       
        for _, category_info in json_data.items():
            json_billing_id=None
           
            if category_info.get("billingAccount") is not None:
                json_billing_id = category_info.get("billingAccount").get("id")
    
            if category_info.get("billingPeriod") is not None:
                json_billingPeriod_endDateTime = category_info.get("billingPeriod").get("endDateTime")
                json_billingPeriod_startDateTime = category_info.get("billingPeriod").get("startDateTime")
           
            json_category = category_info.get("category")
            json_state = category_info.get("state")
           
            
            if ((billingAccount_id == "" or billingAccount_id == json_billing_id) and
               (billingPeriod_endDateTime_gt is None  or (json_billingPeriod_endDateTime and json_billingPeriod_endDateTime >= billingPeriod_endDateTime_gt)) and
                (billingPeriod_startDateTime_lt is None  or (json_billingPeriod_startDateTime and json_billingPeriod_startDateTime <= billingPeriod_startDateTime_lt)) and
                (billingPeriod_endDateTime_lt is None  or (json_billingPeriod_endDateTime and json_billingPeriod_endDateTime <= billingPeriod_endDateTime_lt)) and
                (billingPeriod_startDateTime_gt is None  or (json_billingPeriod_startDateTime and json_billingPeriod_startDateTime >= billingPeriod_startDateTime_gt)) and
                (category == ""  or category == json_category) and
                (state == ""  or state == json_state)
                ):
                extracted_info = {
                    "id": category_info.get("id"),
                    "billNo": category_info.get("billNo"),
                    "billingAccount": category_info.get("billingAccount"),
                    "billingPeriod": category_info.get("billingPeriod"),
                    "category": category_info.get("category"),
                    "state": category_info.get("state")
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
        
        limited_responses_schema = [CustomerBill_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
       
        is_valid=False
        
        is_valid=validate_customer_bill_by_list(json_data, billingAccount_id, category, state) 
                        
        
        if is_valid:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8")
        
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
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
        return raise_exception(status_msg_code, 
                               message, reason, 
                               reference_error, 
                               message_code, 
                               property_path)

