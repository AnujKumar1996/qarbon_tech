import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.common_schemas import EventSubscription
from src.validation.sonata.validating_sellerId_buyerId import (check_buyer_id,
                                                               check_seller_id)
from src.common.exceptions import raise_exception 
  
def retrive_appointment_subscription(id, buyerId, sellerId):
    """
    This function retrieves a hub entity.
    """
    
    try:
        
        current_directory = Path(__file__).parents[1]
        response_file = "appointment_events_subscription.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                     message=f"File not found '{response_file}'",
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
        
        if id in all_keys and json_data.get(id).get('id') == id:
            
            json_result = json_data.get(id)
            
            if buyerId != "" and not check_buyer_id(json_result, buyerId): 
                        return raise_exception(status_msg_code=404, 
                                            message=f"buyerId not found '{buyerId}'", 
                                            reason="buyerId not found", 
                                            reference_error=None, 
                                            message_code= "notFound", 
                                            property_path=None)
                
            if sellerId != ""  and not check_seller_id(json_result, sellerId):
                    return raise_exception(
                        status_msg_code=404, 
                        message= f"sellerId not Found '{sellerId}'",
                        reason="sellerId not Found", 
                        reference_error=None, 
                        message_code="notFound", 
                        property_path=None )        
              
            json_compatible_item_data = jsonable_encoder(EventSubscription(**json_result))
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

