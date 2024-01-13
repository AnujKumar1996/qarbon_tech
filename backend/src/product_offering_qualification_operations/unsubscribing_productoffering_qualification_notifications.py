import json
from pathlib import Path
from fastapi import status,Response
from src.common.exceptions import raise_exception
from src.validation.sonata.validating_sellerId_buyerId import (check_buyer_id,
                                                               check_seller_id)
from src.common.create_jsonfile import delete_record

def unsubscribing_productoffering_qualification_notifications(id, buyerId, sellerId):

    """
    This operation unsubscribes from notifications for the productoffering_qualification_notification APIs.
    """
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "product_offering_qualification_events_subscription.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                    message = f"File not found '{response_file}'" ,
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
        
        all_keys= json_data.keys()  
              
        if id in all_keys:
            json_result = json_data.get(id)
           
            if json_result.get('id') == id:

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
                    
                delete_record(id, file_name)

                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                
            else:
                return raise_exception(status_msg_code=404, 
                                       message="'Id' value mismatch", 
                                       reason="Validation error", 
                                       reference_error= None, 
                                       message_code="notFound", 
                                       property_path=None)
                       
        else:
            return raise_exception(status_msg_code=404,
                                   message=f"Id not found '{id}'", 
                                   reason="'Id' not found",
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
