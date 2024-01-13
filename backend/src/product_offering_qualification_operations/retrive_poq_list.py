import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from src.validation.sonata.validate_product_offering_qualification import validate_list_product_offering_qualification
from src.schemas.sonata_schemas.product_offering_qualification_schema import ProductOfferingQualification_Find
from src.common.exceptions import raise_exception

def retrieve_product_offering_qualification_list(state, externalId, projectId, requestedPOQCompletionDate_gt, requestedPOQCompletionDate_lt, buyerId, sellerId, offset, limit):
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
        
        if offset is None:
            offset = 0
        if limit is None:
            limit = 10

        current_directory = Path(__file__).parents[1]
        response_file = 'product_offering_qualification.json'
        file_name = current_directory / 'responses' / response_file

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found '{response_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(file_name, 'r') as json_file:
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
        for _, poq_info in json_data.items():
            json_state = poq_info.get("state")
            json_externalId = poq_info.get("externalId")
            json_projectId = poq_info.get("projectId")
            json_requestedPOQCompletionDate = poq_info.get("requestedPOQCompletionDate")
            json_buyerId = poq_info.get("buyerId")
            json_sellerId = poq_info.get("sellerId")

            if (
                (state == "" or state == json_state) and
                (externalId == "" or externalId == json_externalId) and
                (projectId == "" or projectId == json_projectId) and
                (requestedPOQCompletionDate_gt is None  or (requestedPOQCompletionDate_gt and requestedPOQCompletionDate_gt <= json_requestedPOQCompletionDate)) and
                (requestedPOQCompletionDate_lt is None  or (requestedPOQCompletionDate_lt and requestedPOQCompletionDate_lt >= json_requestedPOQCompletionDate)) and
                (buyerId == "" or buyerId == json_buyerId) and
                (sellerId == "" or sellerId == json_sellerId)
            ):
                extracted_info = {
                    "id": poq_info.get("id"),
                    "externalId": poq_info.get("externalId"),
                    "state": poq_info.get("state"),
                    "projectId": poq_info.get("projectId"),
                    "requestedPOQCompletionDate": poq_info.get("requestedPOQCompletionDate"),
                }
                extracted_data.append(extracted_info)
        limited_responses = extracted_data[offset: offset + limit]   
        if not limited_responses or not extracted_data:
            status_msg_code = 404
            message = "No matching result found for the given criteria."
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        limited_responses_schema = [ProductOfferingQualification_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)

        validation = validate_list_product_offering_qualification(
            json_data, state, externalId, projectId, requestedPOQCompletionDate_gt,
            requestedPOQCompletionDate_lt, buyerId, sellerId
        )

        if validation is True:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8"
            )
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(
                status_msg_code, message, reason, reference_error, message_code, property_path
            )

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
       
