import json
from pathlib import Path
from fastapi.responses import JSONResponse
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.product_offering_qualification_schema import ProductOfferingQualification
from fastapi.encoders import jsonable_encoder
from fastapi import status
from src.common.create_jsonfile import create_response_json

def modify_product_offering_qualification(order_data, buyerId, sellerId):
    try:
        cwd = Path(__file__).parents[1]
        respnse_file_name = "product_offering_qualification.json"
        poq_response_filename = cwd / "responses" / respnse_file_name

        if not poq_response_filename.exists():
            status_msg_code = 404
            message = f"File not found '{respnse_file_name}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(poq_response_filename, "r") as json_file:
                data_json = json.load(json_file)

        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        found = False
        for order_id, data in data_json.items():
            if found: break 
            for index, existing_item in enumerate(data.get("productOfferingQualificationItem", [])):

                provided_action = order_data["productOfferingQualificationItem"][0]["action"]
                
                if provided_action != "modify":
                    status_msg_code = 422
                    message = "action should be 'modify'"
                    reason = "productOfferingQualificationItem action must be set to 'modify'"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                provided_poq_item_id = order_data["productOfferingQualificationItem"][0]["id"]
                provided_poq_item = order_data["productOfferingQualificationItem"][0]

                if existing_item.get("id") == provided_poq_item_id:
                    found = True
                    # Update productConfiguration based on the provided data
                    existing_buyerId = data.get("buyerId")
                    existing_sellerId = data.get("sellerId")
                    if  buyerId != '' and buyerId != existing_buyerId:
                        status_msg_code = 422
                        message = f"Invalid buyerId '{buyerId}' "
                        reason = "Requested buyerId not Found"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
                    if sellerId != '' and sellerId != existing_sellerId:
                        status_msg_code = 422
                        message = f"Invalid sellerId '{sellerId}'"
                        reason = "Requested buyerId not Found"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
                    if "product" in provided_poq_item and provided_poq_item["product"] is not None and  "id" in provided_poq_item["product"]:
                        product_id = provided_poq_item.get("product").get("id")
                        if product_id is None or product_id.strip() == "":
                            status_msg_code = 422
                            message = "product identifier must not be empty, when 'action' is set to 'modify'"
                            reason = "Product id required for modify"
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
                        reason = "Missing 'product' for 'delete'"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)  
                     

                    if 'relatedContactInformation' in provided_poq_item and provided_poq_item["relatedContactInformation"] is not None:
                        new_contact_info = provided_poq_item['relatedContactInformation'][0]

                        # Check if existing_item['relatedContactInformation'] is None
                        if existing_item['relatedContactInformation'] is None:
                            # If it's None, update it with the new value
                            existing_item['relatedContactInformation'] = [new_contact_info]
                        else:
                            # If it's not None, iterate over the existing contact information and update as needed
                            found_buyer_contact = False
                            for existing_contact_info in existing_item['relatedContactInformation']:
                                if existing_contact_info.get("role") == "buyerContactInformation":
                                    found_buyer_contact = True
                                    # Update specific fields if provided, otherwise keep existing values
                                    for key, value in new_contact_info.items():
                                        if value is not None:
                                            existing_contact_info[key] = value
                                    break

                            if not found_buyer_contact:
                                # If 'buyerContactInformation' is not found, add a new entry
                                existing_item['relatedContactInformation'].append(new_contact_info)

                            # Check if 'role' is 'buyerContactInformation'
                            if new_contact_info.get("role") != "buyerContactInformation":
                                status_msg_code = 422
                                message = "The role in relatedContactInformation must be 'buyerContactInformation'"
                                reason = "Modification is restricted to only the buyer's contact information."
                                reference_error = None
                                message_code = "invalidValue"
                                property_path = None
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                    else:
                        status_msg_code = 422
                        message = "'relatedContactInformation' must not be empty in productOfferingQualificationItem, when 'action' is set to 'modify'."
                        reason = "Valid values are required for relatedContactInformation."
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                    request_productConfiguration = provided_poq_item.get("product").get("productConfiguration")

                    existing_item["product"]["productConfiguration"] = request_productConfiguration

                    existing_item["action"] = provided_poq_item.get("action")
                    
                    # Update the existing item in the data
                    data["productOfferingQualificationItem"][index] = existing_item

                    # Save the modified data back to the JSON file
                    with open(poq_response_filename, 'w') as updated_json_file:
                        json.dump(data_json, updated_json_file, indent=4)

                    # Return the modified order details as the response
                    response_data = jsonable_encoder(ProductOfferingQualification(**data))
                    return JSONResponse(
                        status_code=status.HTTP_201_CREATED,
                        content=response_data,
                        media_type="application/json;charset=utf-8"
                    )

        # If the provided POQ item ID is not found, respond with an error
        status_msg_code = 422
        message = f"Invalid productOfferingQualificationItem id '{provided_poq_item_id}'"
        reason = "Requested productOfferingQualificationItem id not Found"
        reference_error = None
        message_code = "invalidValue"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    except Exception as err:
        # Handle other exceptions as needed
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request."
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
