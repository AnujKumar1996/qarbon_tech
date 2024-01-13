import json
from pathlib import Path
from fastapi import status,Response
from src.common.exceptions import raise_exception
from src.common.validate_datetime import validate_datetime_format
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.catalog_productspecification_schema import ProductSpecification_Find

def retrive_productspecification_list(name, lifecycleStatus, brand,lastUpdate_gt, lastUpdate_lt,buyerId ,sellerId, offset, limit ):
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "catalog_product_specification.json"
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

        date_tuple = (lastUpdate_gt, lastUpdate_lt)
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
            json_name = category_info.get("name")
            json_brand = category_info.get("brand")
            json_lifecycleStatus = category_info.get("lifecycleStatus")
            json_lastUpdate = category_info.get("lastUpdate")
            json_buyerId = category_info.get("buyerId")
            json_sellerId = category_info.get("sellerId")
            
            if ((lifecycleStatus == "" or lifecycleStatus == json_lifecycleStatus) and
                (name == ""  or name == json_name) and
                (brand == ""  or brand == json_brand) and
                (lastUpdate_lt is None  or (lastUpdate_lt and lastUpdate_lt >= json_lastUpdate)) and
                (lastUpdate_gt is None  or (lastUpdate_gt and lastUpdate_gt < json_lastUpdate)) and
                (buyerId == ""  or buyerId == json_buyerId) and
                (sellerId == ""  or sellerId == json_sellerId)
                ):
                extracted_info = {
                    "id": category_info.get("id"),
                    "href": category_info.get("href"),
                    "name": category_info.get("name"),
                    "lastUpdate": category_info.get("lastUpdate"),
                    "lifecycleStatus": category_info.get("lifecycleStatus"),
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
        limited_responses_schema = [ProductSpecification_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=json_data,
            media_type="application/json;charset=utf-8")
    
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

