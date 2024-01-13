import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from src.validation.sonata.validating_sellerId_buyerId import check_seller_id, check_buyer_id
from src.schemas.sonata_schemas.product_offering_qualification_schema import \
    ProductOfferingQualification
from src.common.exceptions import raise_exception
from src.validation.sonata.validate_product_offering_qualification import validate_poq_by_id



def retrieve_product_offering_qualification_by_id(id, buyerId, sellerId):
    try:
        current_directory = Path(__file__).parents[1]
        response_file = 'product_offering_qualification.json'
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found '{response_file}'"
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
        
        all_values = json_data.values()
        found_id =False
        for poq_info in all_values:
            if poq_info["id"] == id:
                found_id =True
                json_result = poq_info
                if buyerId != "" and  not check_buyer_id(json_result, buyerId): 
                        status_msg_code = 404
                        message = f"Invalid buyerId '{buyerId}'"                        
                        reason = "Requested buyerId not found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                if sellerId != "" and not check_seller_id(json_result, sellerId):
                        status_msg_code = 404
                        message = f"Invalid sellerId '{sellerId}'"
                        reason = "Requested sellerId not Found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        if not found_id:   
            status_msg_code = 404
            message = f"Id not found '{id}'"
            reason = "Id not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        json_compatible_item_data = jsonable_encoder(ProductOfferingQualification(**json_result))
        validation = validate_poq_by_id(json_compatible_item_data, id)
        if validation:
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=json_compatible_item_data,
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