
import json
import re
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
from src.schemas.sonata_schemas.common_schemas import EventSubscription
from src.common.exceptions import raise_exception

def subscribe_workorder_notifications(order, buyerId, sellerId):
    """
    This operation sets registration for Notifications.
    """
    try:
        order_data = order.model_dump(by_alias=True)
        current_directory = Path(__file__).parents[1]
        response_file = "workorder_managment_hub.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            return raise_exception(status_msg_code=404, message=f"File not found '{response_file}'", reason="File not found", reference_error=None, message_code="notFound", property_path=None)
        try:                        
            payload_file_name = current_directory / 'common/sonata_payloads.json'
            with open(payload_file_name, "r") as json_file:
                json_payload = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, message="Record not found", reason="Record not found", reference_error=None, message_code="notFound", property_path=None)
        allowed_values = [
            "workOrderCreateEvent",
            "workOrderStateChangeEvent",
            "workOrderAppointmentRequiredEvent"
        ]    
        query_param = order_data.get("query")
        if query_param == "":
            order_data["query"] = "eventType=" + ",".join(allowed_values)
        
        else:
            if "eventType=" not in query_param:
                return raise_exception(status_msg_code=400, message="'eventType' is missing in the query value", reason="eventType is missing in the query value", reference_error=None, message_code="missingQueryParameter", property_path=None)

            if "&" in query_param and "," in query_param:
                return raise_exception(status_msg_code=400, message=f"Invalid query value '{query_param}'", reason="Invalid query value", reference_error=None, message_code="invalidBody", property_path=None)
            
            user_queries_list=re.split("eventType=|&eventType=|,",query_param)
            first_match= user_queries_list[0]
            if first_match !="":
                return raise_exception(status_msg_code=400, message=f"Invalid query value '{first_match}'", reason="Invalid query value", reference_error=None, message_code="invalidBody", property_path=None)
                
            user_queries_list.pop(0)
            for query in set(user_queries_list):
                if query not in allowed_values:
                    return raise_exception(status_msg_code=400, message=f"Invalid query value '{query}'", reason="Invalid query value", reference_error=None, message_code="invalidBody", property_path=None) 
                    
            unique_query_list = list(dict.fromkeys(user_queries_list))
            if len(unique_query_list) != len(user_queries_list):
                if '&' in query_param:
                    order_data["query"] = "eventType=" + "&eventType=".join(unique_query_list)
                else:
                    order_data["query"] = "eventType=" + ",".join(unique_query_list)
        
                
        order_data["id"] = json_payload["events_subscription"]["id"]
        response_data = jsonable_encoder(EventSubscription(**order_data))
        json_response = response_data.copy()
        json_response["buyerId"] = buyerId
        json_response["sellerId"] = sellerId
        if str(order_data.get("callback")) != str(response_data.get("callback")) or order_data.get("query") != response_data.get("query"):
            
            return raise_exception(status_msg_code=400, message="Request and response data are mismatching", reason="Validation error", reference_error=None, message_code="invalidBody", property_path=None)
        create_response_json(order_data["id"], json_response,file_name)  
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                                    content=response_data,
                                    media_type="application/json;charset=utf-8"
                                    )
    except Exception as err:
            return raise_exception(status_msg_code=500,message= str(err), reason="The server encountered an unexpected condition that prevented it from fulfilling the request", reference_error=None, message_code="internalError", property_path=None) 



