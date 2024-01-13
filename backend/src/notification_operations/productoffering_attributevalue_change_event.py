import json
from pathlib import Path
from fastapi import Response, status
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json

def catalog_productoffering_attributevalue_change_event(info):
    try:
        cwd = Path(__file__).parents[1]
        product_category_file="catalog_product_offering.json"
        
        product_category_response_filename = cwd / "responses" / product_category_file
        
        if not product_category_response_filename.exists() :
            status_msg_code = 404
            message = f"File not found '{product_category_file}'"
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
          
        if info.eventType != "productOfferingAttributeValueChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'productOfferingAttributeValueChangeEvent'"
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
            
            current_description = category_data.get("description")
            previous_description = category_data.get("previousDescription")
            
            current_channel = category_data.get("channel")
            previous_channel = category_data.get("previousChannel")
            
            current_region = category_data.get("region")
            previous_region = category_data.get("previousRegion")
            
            current_category = category_data.get("category")
            previous_category = category_data.get("previousCategory")
            
            current_statusTransitions = category_data.get("statusTransitions")
            previous_statusTransitions = category_data.get("previousStatusTransitions")
            
            current_marketSegment = category_data.get("marketSegment")
            previous_marketSegment = category_data.get("previousMarketSegment")
            
            current_note = category_data.get("note")
            previous_note = category_data.get("previousNote")
            
            current_agreement = category_data.get("agreement")
            previous_agreement = category_data.get("previousAgreement")
            
            current_attachment = category_data.get("attachment")
            previous_attachment = category_data.get("previousAttachment")
            
            current_productofferingterm = category_data.get("productOfferingTerm")
            previous_productofferingterm  = category_data.get("previousproductOfferingTerm")
    
            current_relatedcontactinformation = category_data.get("relatedContactInformation")
            previous_relatedcontactinformation = category_data.get("previousrelatedContactInformation")
            
    
            attributes_changed = False
            
            if current_description != previous_description:
                category_data["previousDescription"] = current_description
                attributes_changed = True
                
            if current_channel != previous_channel:
                category_data["previousChannel"] = current_channel
                attributes_changed = True
             
            if current_region != previous_region:
                category_data["previousRegion"] = current_region
                attributes_changed = True   
            
            if current_category != previous_category:
                category_data["previousCategory"] = current_category
                attributes_changed = True
                
            if current_statusTransitions != previous_statusTransitions:
                category_data["previousStatusTransitions"] = current_statusTransitions
                attributes_changed = True       
                
            if current_marketSegment != previous_marketSegment:
                category_data["previousMarketSegment"] = current_marketSegment
                attributes_changed = True       
                
            if current_note != previous_note:
                category_data["previousNote"] = current_note
                attributes_changed = True       
                
            if current_agreement != previous_agreement:
                category_data["previousAgreement"] = current_agreement
                attributes_changed = True       
                
            if current_attachment != previous_attachment:
                category_data["previousAttachment"] = current_attachment
                attributes_changed = True   
                    
            if current_productofferingterm != previous_productofferingterm:
                category_data["previousproductOfferingTerm"] = current_productofferingterm
                attributes_changed = True     
                  
            if current_relatedcontactinformation != previous_relatedcontactinformation:
                category_data["previousrelatedContactInformation"] = current_relatedcontactinformation
                attributes_changed = True       
                
            if attributes_changed :  
                create_response_json(info.event.id, category_data, product_category_response_filename)
                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                
            else:
                status_msg_code = 422
                message = "Product offering attributes values remain unchanged."
                reason = "Validation error"
                reference_error = None
                message_code = "otherIssue"
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


                