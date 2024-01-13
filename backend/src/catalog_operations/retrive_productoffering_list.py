from pathlib import Path
import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.validation.sonata.validate_offering import validate_product_offering_list
from src.common.validate_datetime import validate_datetime_format
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.product_catalog_productoffering_schemas import ProductOffering_Find


def search_in_list_of_dicts(dict_list, key, data):
    for dictionary in dict_list:
        if dictionary.get(key) == data:
            return True
    return False

def retrive_productoffering_list(name, lastUpdate_gt, lastUpdate_lt, lifecycleStatus, agreement ,\
    channel, marketSegment, region_country, category_id, buyerId, sellerId, offset, limit):
    try:
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

        current_directory = Path(__file__).parents[1]
        response_file = 'catalog_product_offering.json'
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found {response_file}"
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
             
        extracted_data = []
        for _, offering_info in json_data.items():
            json_name = offering_info.get("name")
            json_lifecycleStatus = offering_info.get("lifecycleStatus")
            json_lastUpdate = offering_info.get("lastUpdate")
            json_agreement = offering_info.get("agreement")
            json_channel = offering_info.get("channel")
            json_marketSegment = offering_info.get("marketSegment")
            json_region = offering_info.get("region")
            json_category_id = offering_info.get("category")
            json_buyerId = offering_info.get("buyerId")
            json_sellerId = offering_info.get("sellerId")
            if ((lifecycleStatus == "" or lifecycleStatus == json_lifecycleStatus) and
                (name == ""  or name == json_name) and
                (lastUpdate_lt is None  or (lastUpdate_lt and lastUpdate_lt >= json_lastUpdate)) and
                (lastUpdate_gt is None  or (lastUpdate_gt and lastUpdate_gt < json_lastUpdate)) and
                (agreement == ""  or agreement == json_agreement) and
                (channel == ""  or channel in json_channel) and
                (marketSegment == ""  or marketSegment in json_marketSegment) and
                (region_country == ""  or search_in_list_of_dicts(json_region, "country", region_country)) and
                (category_id == ""  or search_in_list_of_dicts(json_category_id, "id", category_id)) and
                (buyerId == ""  or buyerId == json_buyerId) and
                (sellerId == ""  or sellerId == json_sellerId)
                ):
                extracted_info = {
                    "id": offering_info.get("id"),
                    "href": offering_info.get("href"),
                    "name": offering_info.get("name"),
                    "description": offering_info.get("description"),
                    "lastUpdate": offering_info.get("lastUpdate"),
                    "lifecycleStatus": offering_info.get("lifecycleStatus"),
                    "agreement": offering_info.get("agreement"),
                    "channel": offering_info.get("channel"),
                    "marketSegment": offering_info.get("marketSegment"),
                    "region": offering_info.get("region"),
                    "category": offering_info.get("category"),
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
        limited_responses_schema = [ProductOffering_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        validation = validate_product_offering_list(json_data, name, lifecycleStatus, agreement, channel, marketSegment, region_country, category_id, buyerId, sellerId)
        
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