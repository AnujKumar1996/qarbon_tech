import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.common.create_jsonfile import create_response_json
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.product_offering_qualification_schema import ProductOfferingQualification

def disconnect_product_offering_qualification(request_data,buyerId,sellerId):
    
    try:
        current_directory = Path(__file__).parents[1]
        response_file="product_offering_qualification.json"
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
            with open(file_name, "r") as json_file:
                data_json = json.load(json_file)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (empty or invalid JSON)
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        for item in request_data.get("productOfferingQualificationItem"):
            if item.get("action") != "delete":
                status_msg_code = 422
                message = "action should be 'delete'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
            poq_product = item.get("product")
            
            if poq_product.get("productOffering") is not None or poq_product.get("productSpecification") is not None or poq_product.get("productConfiguration") is not None:
                status_msg_code = 422
                message = "when 'action' is set to 'delete' the Buyer must not provide productOffering, productSpecification and productConfiguration attributes"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            poq_product_id = poq_product.get("id")
            if poq_product_id == "":
                status_msg_code = 422
                message = "when 'action' is set to 'delete' the Buyer must provide the product.id of the referenced Product"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        order_response_data = None
        order_response_id = None
        order_response_buyerId = None
        order_response_sellerId = None
        # Extracting ids , actions and product from the request body
        request_ids = {item["id"]: {"action": item["action"], "product": item["product"]} for item in request_data["productOfferingQualificationItem"]}
        # Check if the ids are present in the same order in the response data
        for _, order_data in data_json.items():
            order_ids = {item["id"] for item in order_data.get("productOfferingQualificationItem", [])}
            common_ids = request_ids.keys() & order_ids
            if common_ids == request_ids.keys():  # Check if all requested ids are present in the same order
                # Update the action in the response body for matched ids
                for item in order_data["productOfferingQualificationItem"]:
                    if item["id"] in common_ids:
                        item["action"] = request_ids[item["id"]]["action"]
                        item["product"] = request_ids[item["id"]]["product"]
                        order_response_data = order_data
                        order_response_id = order_data["id"]
                        order_response_buyerId = order_data.get("buyerId")
                        order_response_sellerId = order_data.get("sellerId")
                break  # Exit the loop once the update is done

        # if not all requested ids are present in the same order
        if not set(request_ids.keys()).issubset(common_ids):
            status_msg_code = 422
            message = "productOfferingQualificationItem Id not found"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if buyerId != "" and  order_response_buyerId != buyerId:
            status_msg_code = 422
            message = f"Invalid buyerId '{buyerId}' "
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if sellerId != "" and  order_response_sellerId != sellerId:
            status_msg_code = 422
            message = f"Invalid sellerId '{sellerId}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        response_data = jsonable_encoder(ProductOfferingQualification(**order_response_data))
        

        create_response_json(order_response_id, order_response_data, file_name)   
            
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=response_data,
                                media_type="application/json;charset=utf-8"
                                )  
        
    except ValidationError as e:
        status_msg_code = 422
        message = str(e)
        reason = "Validation error"
        reference_error = None
        message_code = "invalidValue"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
    except Exception as e:
        status_msg_code = 500
        message = str(e)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path= None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
              