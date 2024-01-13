import json
from pathlib import Path

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.call_external_apis.call_qcl_deinstall_api import call_deinstall_api
from src.common.exceptions import raise_exception
from requests.models import Response as reqres
from starlette.responses import JSONResponse 
from fastapi import status
from src.common.qcl_error_handling import handle_qcl_error
from src.common.extract_error_message import extract_error_msg
from src.field_mapping.map_deinstall_fields import map_deinstall_fields
from src.schemas.interlude_schemas.error_schemas import (Error404, Error422,
                                                         Error500)
from src.schemas.sonata_schemas.common_schemas import ProductOrder
from src.validation.sonata.delete_product_order_validation import \
    delete_product_order_validation
from src.common.create_jsonfile import update_lattice_id


def disconnect_product_order(order_data, action, buyerId, sellerId, ccLoaAttachmentId, token, refresh_token):
    try:
        allowed_buyerIds = ("ONS", "ZOH", "SLF","QLP")
        if buyerId not in allowed_buyerIds:
            status_msg_code = 422
            message = "Invalid 'buyerId'"
            reason = "Invalid value"
            reference_error = "https://docs.pydantic.dev/latest/errors/validation_errors/"
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        allowed_sellerIds = ("EQX", "CYX")
        if sellerId not in allowed_sellerIds:
            status_msg_code = 422
            message = "Invalid 'sellerId'"
            reason = "Invalid value"
            reference_error = "https://docs.pydantic.dev/latest/errors/validation_errors/"
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        
        current_directory = Path(__file__).parents[1]
        response_file="sonata_response.json"
        file_name = current_directory / 'responses' / response_file
        if not file_name.exists():
            return raise_exception(status_msg_code=404, message=f"File not found '{response_file}'", reason="File not found", reference_error=None, message_code="notFound", property_path=None)
        try:
            with open(file_name, "r") as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError as e:
           return raise_exception(status_msg_code=404, message="Record not found", reason="Record not found", reference_error=None, message_code="notFound", property_path=None)
        
        payload_file="sonata_payloads.json"            
        payload_file_name = current_directory / 'common'/ payload_file
        if not payload_file_name.exists():
            status_msg_code = 404
            message = f"File not found: '{payload_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        try:    
            with open(payload_file_name, "r") as json_file:
                json_payload = json.load(json_file)
                
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Records not found"
            reason = "Records not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        provided_product_order_item = order_data["productOrderItem"][0]
        
        is_item_present = False  # Initialize the flag here
        
        for existing_order_id, json_data in data.items():
            if is_item_present: break
                
            existing_order = json_data
            for index, existing_item in enumerate(existing_order.get("productOrderItem")):
           
                if existing_item["id"] == provided_product_order_item["id"]:
                    
                    if  buyerId != '' and buyerId != json_data.get("buyerId"):
                        status_msg_code = 422
                        message = f"Invalid buyerId '{buyerId}' "
                        reason = "Requested buyerId not Found"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
                    if sellerId != '' and sellerId != json_data.get("sellerId"):
                        status_msg_code = 422
                        message = f"Invalid sellerId '{sellerId}'"
                        reason = "Requested sellerId not Found"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
                    # productorder_id = provided_product_order_item["id"]
                    # if existing_item["action"] == "delete":
                    #     # Product order is already disconnected
                    #     error_data = {
                    #         "message": f"Invalid productOrderItem identifier, product order is already disconnected for productOrderItem identifier {productorder_id}",
                    #         "reason": "Validation error",
                    #         "referenceError": "https://example.com",
                    #         "code": "invalidValue",
                    #         "propertyPath": "productOrderItem.id"
                    #         }
                    #     response_data = jsonable_encoder(Error422(**error_data))
                    #     return JSONResponse(
                    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #         content=response_data,
                    #         media_type="application/json;charset=utf-8"
                    #     )
                    
                    if provided_product_order_item["action"] != "delete":
                        status_msg_code = 422
                        message = "productOrderItem.action should be 'delete'"
                        reason = "Validation error"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)       
                        
                    existing_item["action"] = provided_product_order_item["action"]
                    
                 
                    # Validate product.id is provided and not empty
                    if "product" in provided_product_order_item and provided_product_order_item["product"] is not None and  "id" in provided_product_order_item["product"]:
                        product_id = provided_product_order_item["product"]["id"]
                        if product_id is None or product_id.strip() == "":
                            status_msg_code = 422
                            message = "product identifier must not be empty, when 'action' is set to 'delete'"
                            reason = "Validation error"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    
                        
                            # If "product" is None, create it with an "id"
                        if existing_item["product"] is None:
                            existing_item["product"] = {"id": product_id}
                        else:
                            existing_item["product"]["id"] = product_id
                    else:
                        status_msg_code = 422
                        message = "'product' must be provided, when 'action' is set to 'delete'"
                        reason = "Validation error"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)  
                    
                    order_item_state = json_payload["productorder_disconnect"]["state"]
                    existing_item['state'] = order_item_state 
                        
                    existing_order["productOrderItem"][index] = existing_item
                    
                    is_item_present = True  # Set the flag to True if the item is found
                    break
                
                    # /----------------
                    # if "requestedItemTerm" not in provided_product_order_item:
                    #     error_data = {
                    #         "message": "'requestedItemTerm' must be provided in the request body",
                    #         "reason": "Validation error",
                    #         "referenceError": "https://example.com",
                    #         "code": "invalidValue",
                    #         "propertyPath": "requestedItemTerm"
                    #     }
                    #     response_data = jsonable_encoder(Error422(**error_data))
                    #     return JSONResponse(
                    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #         content=response_data,
                    #         media_type="application/json;charset=utf-8"
                    #     )    
                    
                    # requested_item_term = provided_product_order_item.get("requestedItemTerm")
                    # if requested_item_term:
                    #     existing_item["requestedItemTerm"] = {
                    #         "description": existing_item["requestedItemTerm"].get("description", ""),
                    #         "name": requested_item_term["name"],
                    #         "endOfTermAction": requested_item_term["endOfTermAction"],
                    #         "duration": requested_item_term["duration"],
                    #         "rollInterval": requested_item_term.get("rollInterval", {})
                    #     }
                        
                    #     # Validate End of Term Action
                    #     valid_end_of_term_actions = ["roll", "autoDisconnect", "autoRenew"]
                    #     end_of_term_action = requested_item_term["endOfTermAction"]
                    #     if end_of_term_action not in valid_end_of_term_actions:
                    #         error_data = {
                    #             "message": f"Invalid 'endOfTermAction': {end_of_term_action}",
                    #             "reason": "Validation error",
                    #             "referenceError": "https://example.com",
                    #             "code": "invalidValue",
                    #             "propertyPath": "requestedItemTerm.endOfTermAction"
                    #         }
                    #         response_data = jsonable_encoder(Error422(**error_data))
                    #         return JSONResponse(
                    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #             content=response_data,
                    #             media_type="application/json;charset=utf-8"
                    #         )
                
                    #     # Validate Roll Interval if endOfTermAction is "roll"
                    #     if end_of_term_action == "roll":
                    #         roll_interval = requested_item_term.get("rollInterval")
                    #         if not roll_interval or not roll_interval.get("amount") or not roll_interval.get("units"):
                    #             error_data = {
                    #                 "message": "'The Buyer must provide the 'rollInterval' if the 'endOfTermAction' is set to 'roll'.'",
                    #                 "reason": "Validation error",
                    #                 "referenceError": "https://example.com",
                    #                 "code": "invalidValue",
                    #                 "propertyPath": "requestedItemTerm.rollInterval"
                    #             }
                    #             response_data = jsonable_encoder(Error422(**error_data))
                    #             return JSONResponse(
                    #                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #                 content=response_data,
                    #                 media_type="application/json;charset=utf-8"
                    #             )
                            
                    #         roll_amount = roll_interval["amount"]
                            
                    #         if roll_amount < 0:
                    #             error_data = {
                    #                 "message": "'rollInterval.amount' should be positive",
                    #                 "reason": "Validation error",
                    #                 "referenceError": "https://example.com",
                    #                 "code": "invalidValue",
                    #                 "propertyPath": "requestedItemTerm.rollInterval.amount"
                    #             }
                    #             response_data = jsonable_encoder(Error422(**error_data))
                    #             return JSONResponse(
                    #                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #                 content=response_data,
                    #                 media_type="application/json;charset=utf-8"
                    #             )
                    
                    # duration = requested_item_term.get("duration")
                    # if duration and duration.get("amount") and duration.get("units"):
                    #     duration_amount = duration["amount"]
                    #     if duration_amount < 0:
                    #         error_data = {
                    #             "message": "'duration.amount' should be positive value",
                    #             "reason": "Validation error",
                    #             "referenceError": "https://example.com",
                    #             "code": "invalidValue",
                    #             "propertyPath": "requestedItemTerm.duration.amount"
                    #         }
                    #         response_data = jsonable_encoder(Error422(**error_data))
                    #         return JSONResponse(
                    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    #             content=response_data,
                    #             media_type="application/json;charset=utf-8"
                    #         )
                    #     existing_item["requestedItemTerm"]["duration"] = {
                    #         "amount": duration_amount,
                    #         "units": duration["units"]
                    #     }
                    
                    
        if is_item_present:
            
            token_type_val = token.scheme
            token_val = token.credentials
            
            is_mapped, msg_statuscode, mapped_data, reason, reference_error, message_code, property_path = map_deinstall_fields(order_data, buyerId, sellerId,ccLoaAttachmentId)
            
            
            if not is_mapped and isinstance(mapped_data, str):
                return raise_exception(msg_statuscode, mapped_data, reason, reference_error, message_code, property_path)
            
            
            qcl_response = call_deinstall_api(mapped_data, token_val, refresh_token, token_type_val)
            
            response = handle_qcl_error(qcl_response,refresh_token,mapped_data,call_deinstall_api)
                        
            if isinstance(response, reqres):
                if response.status_code == 201:
                    qcl_response = response
                else:
                    return handle_qcl_error(response,refresh_token,mapped_data,call_deinstall_api)
            
            elif isinstance(response, JSONResponse):
                return response
            
                
            
            qcl_response = qcl_response.json()
            lattice_id = qcl_response.get("lattice_transaction_id")
            existing_order["id"] = lattice_id
            
            response_data = jsonable_encoder(ProductOrder(**existing_order))
            result = delete_product_order_validation(order_data,response_data)
            
            if result:
                
                if not update_lattice_id(lattice_id, 'order'):
                    status_msg_code = 422
                    message = f"Unable to update JSON file with lattice_transaction_id {lattice_id}"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "otherIssue"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                with open(file_name, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                
                # Return the modified order details as the response
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=response_data,
                    media_type="application/json;charset=utf-8"
                )
            else:
                status_msg_code = 422
                message = "Request and Response data are mismatching"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            # If no matching item is found, return an error response
            status_msg_code = 422
            message = "productOrderItem identifier not found"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
    except ValidationError as e:
        status_msg_code = 422
        message = str(e)
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
