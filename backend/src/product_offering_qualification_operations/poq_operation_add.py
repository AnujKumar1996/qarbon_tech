import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.common.create_jsonfile import create_response_json
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.product_offering_qualification_schema import ProductOfferingQualification

def create_product_offering_qualification(order_data, buyerId, sellerId):
    
    try:
        if order_data.get("instantSyncQualification") is False and order_data.get("requestedPOQCompletionDate") is None:
            status_msg_code = 422
            message = "The requestedPOQCompletionDate MUST be specified when instantSyncQualification=false"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        for items in order_data.get("relatedContactInformation"):
            if items.get("role") != "buyerContactInformation" :
                status_msg_code = 422
                message = "The Buyer's request MUST specify a relatedContactInformation item with a role set to buyerContactInformation"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        poq_ids = set()
        for item in order_data.get("productOfferingQualificationItem"):
            if item.get("action") != "add":
                status_msg_code = 422
                message = "action should be 'add'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            poq_id = item.get("id")
            if poq_id in poq_ids:
                status_msg_code = 422
                message = "productOfferingQualificationItem 'Id' can't be duplicate. It must be unique for same productOfferingQualificationItem"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            poq_ids.add(poq_id)
            
            product = item.get("product")
            productspecification = product.get("productSpecification")
            productoffering = product.get("productOffering")
            productconfiguration = product.get("productConfiguration")
            product_id = product.get("id")
            
            if productspecification is None and productoffering is None:
                status_msg_code = 422
                message = "The Buyer MUST provide the productspecification or productoffering"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if productconfiguration is None:
                status_msg_code = 422
                message = "The Buyer MUST provide the productconfiguration"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            if product_id != "":
                status_msg_code = 422
                message = "if action=add the Buyer MUST NOT provide product.id"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
        current_directory = Path(__file__).parents[1]
        file_name = current_directory / 'responses/product_offering_qualification.json'
        
        payload_file_name = current_directory / 'common/sonata_payloads.json'
        with open(payload_file_name, "r") as json_file:
            json_payload = json.load(json_file)

        order_data["state"] = json_payload.get("poq_payload").get("state")
    
        for order_status in order_data.get("productOfferingQualificationItem"):
            order_status["state"]=json_payload["poq_payload"]["productOfferingQualificationItem"][0]["state"]
        
        order_data["id"]  =  json_payload["poq_payload"]["id"] 
        
        response_data = jsonable_encoder(ProductOfferingQualification(**order_data))
        json_response = response_data.copy()
        json_response["buyerId"] = buyerId
        json_response["sellerId"] = sellerId
        json_response["previoustate"] = order_data["state"]
        
        # for product_status in json_response.get("productOfferingQualificationItem"):
        #     product_status["previoustate"] = sonata_extra_payload["poq_payload"]["productOfferingQualificationItem"][0]["state"]
        
        create_response_json(order_data["id"], json_response, file_name)   
                
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
            
        
        
            
                
            
        

                
        
        