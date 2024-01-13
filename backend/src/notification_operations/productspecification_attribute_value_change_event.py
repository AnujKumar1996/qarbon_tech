import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json

def productspecification_attribute_value_change_event(info):

    try:
        cwd = Path(__file__).parents[1]
        product_specification_file = "catalog_product_specification.json"
        product_specification_response_filename = cwd / "responses" / product_specification_file 
        
        if not product_specification_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{product_specification_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(product_specification_response_filename, "r") as json_file:
                data_json = json.load(json_file)
        
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "productSpecificationAttributeValueChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'productSpecificationAttributeValueChangeEvent'"
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
            product_specification_data=data_json[info.event.id]
            
            if info.event.sellerId != "" and product_specification_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.sellerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            if info.event.buyerId != "" and product_specification_data["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.buyerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and product_specification_data["href"] != info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.href"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            current_description = product_specification_data.get("description")
            previous_description = product_specification_data.get("previousDescription")
            
            current_attachment = product_specification_data.get("attachment")
            previous_attachment = product_specification_data.get("previousAttachment")
            
            current_note = product_specification_data.get("note")
            previous_note = product_specification_data.get("previousNote")
            
            current_productSpecificationRelationship = product_specification_data.get("productSpecificationRelationship")
            previous_productSpecificationRelationship = product_specification_data.get("previousProductSpecificationRelationship")
            
            attributes_changed = False
            
            if current_description != previous_description:
                product_specification_data["previousDescription"] = current_description
                attributes_changed = True
               
            if current_attachment != previous_attachment:
                product_specification_data["previousAttachment"] = current_attachment
                attributes_changed = True
           
            if current_note != previous_note:
                product_specification_data["previousNote"] = current_note
                attributes_changed = True
            
            if current_productSpecificationRelationship != previous_productSpecificationRelationship:
                product_specification_data["previousProductSpecificationRelationship"] = current_productSpecificationRelationship
                attributes_changed = True
            
            if attributes_changed:
               create_response_json(info.event.id, product_specification_data, product_specification_response_filename)
               return Response(status_code = status.HTTP_204_NO_CONTENT,media_type = "application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "Product specification attributes remain unchanged."
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


                