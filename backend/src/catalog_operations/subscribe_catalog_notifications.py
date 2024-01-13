
import json
import re
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
from src.schemas.sonata_schemas.common_schemas import EventSubscription
from src.common.exceptions import raise_exception

def subscribe_catalog_notifications(order, buyerId, sellerId):
    """
    This operation sets registration for Notifications.
    """
    try:
        order_data = order.model_dump(by_alias=True)
        
        current_directory = Path(__file__).parents[1]
        file_name = current_directory / 'responses/catalog_events_subscription.json'

             
        allowed_values = [
            
            "categoryCreateEvent",
            "categoryAttributeValueChangeEvent",
            "categoryStatusChangeEvent",
            "productOfferingCreateEvent",
            "productOfferingAttributeValueChangeEvent",
            "productOfferingStatusChangeEvent",
            "productSpecificationCreateEvent",
            "productSpecificationAttributeValueChangeEvent",
            "productSpecificationStatusChangeEvent"
        ] 
           
        query_param = order_data.get("query")
        
        if query_param == "":
            order_data["query"] = "eventType=" + ",".join(allowed_values)
        
        else: 
               
            if query_param != "" and "eventType=" not in query_param:
                
                status_msg_code = 400
                message = "'eventType' is missing in the query value"
                reason = "eventType is missing"
                reference_error = None
                message_code = "missingQueryParameter"
                property_path = None
            
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            
            user_query = query_param.split('=')[0].strip()
            if query_param != "" and user_query != "eventType" :
                    
                    status_msg_code = 400
                    message = f"Invalid query value '{user_query}'"
                    reason = "Invalid query value"
                    reference_error = None
                    message_code = "invalidBody"
                    property_path = None

                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
    
            if query_param != ""  and ',' in query_param:
            
                user_queries=query_param.split('=')[1].strip()
                user_query_list = user_queries.split(',')
                
                if len(user_query_list) != len(set(user_query_list)):
                    status_msg_code = 400
                    message = "Duplicate query values are not allowed"
                    reason = "Duplicate query values"
                    reference_error = None
                    message_code = "invalidBody"
                    property_path = None
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            
                for query in user_query_list:
                    if query not in allowed_values:
                        
                        status_msg_code = 400
                        message = f"Invalid query value '{query}'"
                        reason = "Invalid query value"
                        reference_error = None
                        message_code = "invalidBody"
                        property_path = None
                    
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            
            elif query_param != "" and '&' in query_param:
                user_query_list = query_param.split('&')
                for query in user_query_list :
                    user_query_list = query.split('=')[1].strip()
                    
                    if user_query_list not in allowed_values:
                    
                        status_msg_code = 400
                        message = f"Invalid query value '{user_query_list}'"
                        reason = "Invalid query value"
                        reference_error = None
                        message_code = "invalidBody"
                        property_path = None
                    
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                

            elif query_param != "":

                user_query_list = query_param.split('=')[1].strip()

                if re.search('[^a-zA-Z]', user_query_list) is None:
                
                    if user_query_list not in allowed_values:
                    
                        status_msg_code = 400
                        message = f"Invalid query value '{user_query_list}'"
                        reason = "Invalid query value"
                        reference_error = None
                        message_code = "invalidBody"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            
                else:

                    status_msg_code = 400
                    message = f"Invalid query value '{user_query_list}'"
                    reason = "Invalid query value"
                    reference_error = None
                    message_code = "invalidBody"
                    property_path = None
                
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        
        try:
            payload_file_name = current_directory / 'common/sonata_payloads.json'
            with open(payload_file_name, "r") as json_file:
                json_payload = json.load(json_file)
        
        except:
           return raise_exception(status_msg_code=404, 
                                    message=f"unable to read '{payload_file_name}'",
                                    reason="Data not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)    
            
            
        order_data["id"] = json_payload["events_subscription"]["id"]
        response_data = jsonable_encoder(EventSubscription(**order_data))
        
      
        if str(order_data.get("callback")) != str(response_data.get("callback")) or order_data.get("query") != response_data.get("query"):
            
            status_msg_code = 400
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

       
        json_response = response_data.copy()
        json_response["buyerId"] = buyerId
        json_response["sellerId"] = sellerId
       
        create_response_json(order_data["id"], json_response,file_name)  
       
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                                    content=response_data,
                                    media_type="application/json;charset=utf-8"
                                    )
    except Exception as err:
        
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
       
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 



