import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from src.validation.sonata.validate_workorder import validate_list_workorder
from src.schemas.sonata_schemas.work_order_schemas import \
    WorkOrder_Find
from src.common.exceptions import raise_exception
def search_in_list_of_objects(obj_list, key, data):
        for obj in obj_list:
            if obj.get(key) == data:
                return True
        return False

def retrive_workorder_list(geographicalSiteId, geographicalAddressId, relatedEntityType, relatedEntityId, state, appointmentRequired, buyerId, sellerId, offset, limit):
    try:
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
        response_file = 'workorder.json'
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

        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        extracted_data = []
        for _, workorder_info in json_data.items():
            json_place = workorder_info.get("place")
            json_relatedEntity = workorder_info.get("relatedEntity")
            json_state = workorder_info.get("state")
            json_appointmentRequired = workorder_info.get("appointmentRequired")
            json_buyerId = workorder_info.get("buyerId")
            json_sellerId = workorder_info.get("sellerId")
            if ((geographicalSiteId == "" or search_in_list_of_objects(json_place,"geographicalSiteId",geographicalSiteId)) and
                (geographicalAddressId == "" or search_in_list_of_objects(json_place,"geographicalAddressId",geographicalAddressId)) and
                (relatedEntityType == "" or search_in_list_of_objects(json_relatedEntity,"@referredType",relatedEntityType)) and
                (relatedEntityId == "" or search_in_list_of_objects(json_relatedEntity,"id",relatedEntityId)) and
                (state == "" or state == json_state) and
                (appointmentRequired is None or appointmentRequired == json_appointmentRequired) and
                (buyerId == "" or buyerId == json_buyerId) and
                (sellerId == "" or sellerId == json_sellerId)):
                extracted_info = {
                "id": workorder_info.get("id"),
                "appointmentRequired": workorder_info.get("appointmentRequired"),
                "place": workorder_info.get("place"),
                "relatedEntity": workorder_info.get("relatedEntity"),
                "state": workorder_info.get("state"),
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
        
        limited_responses_schema = [WorkOrder_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        validation = validate_list_workorder(json_data, relatedEntityType, relatedEntityId, state, appointmentRequired)

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
        return raise_exception(status_msg_code, 
                               message, reason, 
                               reference_error, 
                               message_code, 
                               property_path)