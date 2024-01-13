
import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.validation.sonata.validating_sellerId_buyerId import (check_buyer_id,
                                                               check_seller_id)
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.product_catalog_productoffering_schemas import ProductOffering

def retrive_productoffering(id, buyerId, sellerId):
    
    """
    This operation retrieves productOffering details.
    """
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "catalog_product_offering.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                    message=f"File not found {response_file}",
                                    reason="File not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                   message="Record not found", 
                                   reason="Record not found", 
                                   reference_error=None, 
                                   message_code="notFound", 
                                   property_path=None)        
        all_keys = json_data.keys()  
        
        if id in all_keys:
            json_result = json_data.get(id)
            
            if buyerId != "":
                if not check_buyer_id(json_result, buyerId): 
                   
                    return raise_exception(status_msg_code=404, 
                                                   message=f"buyerId not found '{buyerId}'", 
                                                   reason="buyerId not found", 
                                                   reference_error=None, 
                                                   message_code= "notFound", 
                                                   property_path=None)
            
            if sellerId != "":
                if not check_seller_id(json_result, sellerId):
                    
                    return raise_exception(
                                status_msg_code=404, 
                                message= f"sellerId not Found '{sellerId}'",
                                reason="sellerId not Found", 
                                reference_error=None, 
                                message_code="notFound", 
                                property_path=None )
            
            required_fields = ["id", "name", "description", "lastUpdate", "lifecycleStatus", "productOfferingSpecification",
                                "productSpecification", "statusTransitions", "productOfferingStatusReason", "agreement", "attachment",
                                "relatedContactInformation", "channel", "marketSegment", "region", "productOfferingTerm", "note", "category", "productOfferingContextualInfo"]
         
            for field in required_fields:
                if field not in json_result:
                   
                    return raise_exception(status_msg_code=404, 
                                           message=f"Field '{field}' is missing in the response",
                                             reason="Field is missing", 
                                             reference_error=None, 
                                             message_code='notFound', 
                                             property_path=None)
            
            if ("schema" in json_result.get("productOfferingSpecification") and "schemaLocation" in json_result.get("productOfferingSpecification")) or ("schema" not in json_result.get("productOfferingSpecification") and "schemaLocation" not in json_result.get("productOfferingSpecification")):
                
                return raise_exception(status_msg_code=404, 
                                       message="The Seller response must include exactly one of the 'schema' or 'schemaLocation' attributes", 
                                       reason="validation Error", 
                                       reference_error=None, 
                                       message_code="notFound", 
                                       property_path=None)
            
            data_list = json_result.get("productOfferingContextualInfo")
            for item in data_list:
                context_schema = item.get('contextSchema')

                if ("schema" in context_schema and "schemaLocation" in context_schema) or ("schema" not in context_schema and "schemaLocation" not in context_schema):
                  
                    return raise_exception(status_msg_code=404, 
                                       message="The Seller response must include exactly one of the 'schema' or 'schemaLocation' attributes",
                                       reason="validation Error", 
                                       reference_error=None, 
                                       message_code="notFound", 
                                       property_path=None)

            json_compatible_item_data = jsonable_encoder(ProductOffering(**json_result))
            return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_item_data,media_type="application/json;charset=utf-8")  
        
                                   
        else:
            
            return raise_exception(status_msg_code=404,
                                   message=f"Id not found '{id}'", 
                                   reason="Id not found",
                                   reference_error=None,
                                   message_code="notFound",
                                   property_path=None)

    except Exception as err:
            return raise_exception(status_msg_code=500,
                                   message= str(err), 
                                   reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                   reference_error=None, 
                                   message_code="internalError", 
                                   property_path=None) 

