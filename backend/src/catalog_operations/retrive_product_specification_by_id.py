import json
from pathlib import Path
from fastapi import status
from src.common.exceptions import raise_exception
from src.validation.sonata.validate_product_specification import validate_product_specification_by_id
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.catalog_productspecification_schema import ProductSpecification

def get_product_specification_by_id(id, buyerId, sellerId):
    try:
        if id:
            cwd = Path(__file__).parents[1]
            response_file="catalog_product_specification.json"
            fileName = cwd / 'responses' / response_file
            if not fileName.exists():
                status_msg_code = 404
                message = f"File not found {response_file}"
                reason = "File not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            try:
                with open(fileName,'r') as json_file:
                    json_data = json.load(json_file)
            except json.JSONDecodeError:
                status_msg_code = 404
                message = "Record not found"
                reason = "Record not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                                        
            if id in json_data:
                order_info = json_data[id]
                # Check if buyerId and sellerId are provided
                
                if buyerId != "" and buyerId != order_info.get("buyerId"): 
                    
                        status_msg_code = 404
                        message = f"Invalid buyerId '{buyerId}'"
                        reason = "Requested buyerId not found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                if sellerId != "" and  sellerId != order_info.get("sellerId"): 
                    
                        status_msg_code = 404
                        message = f"Invalid sellerId '{sellerId}'"
                        reason = "Requested sellerId not Found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                json_compatible_item_data = jsonable_encoder(ProductSpecification(**order_info))
                    
                result = validate_product_specification_by_id(order_info, id)  
                if result:
                    return JSONResponse(
                        status_code = status.HTTP_200_OK,
                        content = json_compatible_item_data,
                        media_type="application/json;charset=utf-8"
                    )
                else:
                    status_msg_code = 422
                    message = "Request and Response data mismatch."
                    reason = "Validation error"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            else:   
                status_msg_code = 404
                message = f"Id not found '{id}'"
                reason = "Id not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        else:
            # If 'id' is missing in the query parameters, return a 400 (Bad Request) 
            status_msg_code = 400
            message = f"Invalid or empty 'id' {id}"
            reason = "Bad request"
            reference_error = None
            message_code = "missingQueryValue"
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



