from pathlib import Path
import json
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.geographicaddressmanagement_schema import GeographicAddressValidation
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import create_response_json
from src.validation.sonata.validate_geographicaddress import validate_geographicaddress

def create_geographicaddress_validation(order, buyerId, sellerId):
    
    """
     Create and validate a geographic address based on the provided order data.  
    """
    try:
        order_data=order.model_dump(by_alias=True)
        
        current_directory = Path(__file__).parents[1]
        response_file = "geographicaddress_management_geographicaddress_validation.json"
        file_name = current_directory / 'responses'/response_file
        
        
        sonata_payloads = current_directory / 'common/sonata_payloads.json'
        
        if not sonata_payloads.exists():
            return raise_exception(status_msg_code=404,
                            message=f"File not found '{response_file}'",
                            reason="File not found", 
                            reference_error=None, 
                            message_code="notFound", 
                            property_path=None)
        
        try:
            with open(sonata_payloads, "r") as json_file:
                json_payload = json.load(json_file)
                
        
        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)        
                  
                  
        if order_data['provideAlternative'] == False:
            status_msg_code = 422
            message = "The buyer must always set the value of 'provideAlternative' to true."
            reason = "Incorrect value assigned to 'provideAlternative'."
            reference_error = None
            message_code = "otherIssue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
        order_data["id"] = json_payload.get("geographicvalidationadress_payload").get("id")  
        order_data["validationResult"] = json_payload.get("geographicvalidationadress_payload").get("validationResult") 
        order_data['alternateGeographicAddress'] = json_payload.get("geographicvalidationadress_payload", {}).get("alternateGeographicAddress")
        order_data['bestMatchGeographicAddress'] = json_payload.get("geographicvalidationadress_payload", {}).get("bestMatchGeographicAddress")
        
        response_data = jsonable_encoder(GeographicAddressValidation(**order_data))
        
        json_response = response_data.copy()
        json_response["buyerId"] = buyerId
        json_response["sellerId"] = sellerId
        
        is_valid=validate_geographicaddress(response_data, order_data)
        
        if is_valid:
            
            create_response_json(order_data["id"], json_response,file_name) 
            
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                    content=response_data,
                                    media_type="application/json;charset=utf-8"
                                    )
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
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
      