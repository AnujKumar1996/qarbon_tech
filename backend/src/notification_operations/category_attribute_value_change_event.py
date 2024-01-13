import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json

def category_attributevalue_change_event(info):

    try:
        cwd = Path(__file__).parents[1]
        category_response_file = "catalog_category_response.json"
        product_category_response_filename = cwd / "responses" / category_response_file 
        
        if not product_category_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{category_response_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(product_category_response_filename, "r") as json_file:
                data_json = json.load(json_file)
        
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "categoryAttributeValueChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'categoryAttributeValueChangeEvent'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "eventType"
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
        list_of_keys = data_json.keys()  
        
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "event.id"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        else:
            product_category_data = data_json[info.event.id]
            
            if info.event.sellerId != "" and product_category_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.sellerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            if info.event.buyerId != "" and product_category_data["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.buyerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and product_category_data["href"] != info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.href"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            current_description = product_category_data.get("description")
            previous_description = product_category_data.get("previousDescription")
            
            current_parentCategory = product_category_data.get("parentCategory")
            previous_parentCategory = product_category_data.get("previousParentCategory")
            
            current_subCategory = product_category_data.get("subCategory")
            previous_subCategory = product_category_data.get("previousSubCategory")
            
            current_productOffering = product_category_data.get("productOffering")
            previous_productOffering = product_category_data.get("previousProductOffering")
            
            attributes_changed = False
            
            if current_description != previous_description:
                product_category_data["previousDescription"] = current_description
                attributes_changed = True
               
            if current_parentCategory != previous_parentCategory:
                product_category_data["previousParentCategory"] = current_parentCategory
                attributes_changed = True
           
            if current_subCategory != previous_subCategory:
                product_category_data["previousSubCategory"] = current_subCategory
                attributes_changed = True
            
            if current_productOffering != previous_productOffering:
                product_category_data["previousProductOffering"] = current_productOffering
                attributes_changed = True
            
            if attributes_changed:
               create_response_json(info.event.id, product_category_data, product_category_response_filename)
               return Response(status_code = status.HTTP_204_NO_CONTENT,media_type = "application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "Product category attributes values remain unchanged."
                reason = "Validation error"
                reference_error = None
                message_code = "otherIssue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request."
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


                