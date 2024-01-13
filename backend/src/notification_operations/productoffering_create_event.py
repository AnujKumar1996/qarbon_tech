import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception

def productoffering_create_event_notification(info):

    try:
        cwd = Path(__file__).parents[1]
        product_offering_file="catalog_product_offering.json"
        
        product_offering_response_filename = cwd / "responses" / product_offering_file 
        
        if not product_offering_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{product_offering_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(product_offering_response_filename, "r") as json_file:
                data_json = json.load(json_file)
        
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        if info.eventType != "productOfferingCreateEvent":
            status_msg_code = 422
            message = "The eventType must be 'productOfferingCreateEvent'"
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
            category_data=data_json[info.event.id]
            
            if info.event.sellerId != "" and category_data["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.sellerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                    
            if info.event.buyerId != "" and category_data["buyerId"]!=info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.buyerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and category_data["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.href"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


                