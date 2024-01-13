import json
import re
from pathlib import Path
from typing import Union

from fastapi import APIRouter, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
                                        
from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500, Error501)
from src.schemas.sonata_schemas.common_schemas import (EventSubscription,
                                                       EventSubscriptionInput)
from src.validation.sonata.validating_sellerId_buyerId import (check_buyer_id,
                                                               check_seller_id)

from .response_headers import add_headers
from src.common.exceptions import raise_exception
from src.common.create_jsonfile import delete_record

router = APIRouter( prefix="/v1/MEF/lsoSonata/productOrderingManagement",tags=["productOrder Events Subscription"])

@router.post('/hub',
            response_model=Union[EventSubscription, Error400, Error401, Error403,  Error500,Error501],
            status_code=201,
            responses={
                
                201: common_schema["hub_response_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )

async def create_hub(
    order: EventSubscriptionInput,
    response: Response,

    buyerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer. \
            Reference: MEF 79 (Sn 8.8)",
        ),

    sellerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when the responding entity represents more than one Seller. \
            Reference: MEF 79 (Sn 8.8)"
        )
    ):
    """
    This operation sets registration for Notifications.
    """
    try:
        add_headers(response)
        order_data = order.model_dump(by_alias=True)
        
        current_directory = Path(__file__).parents[1]
        file_name = current_directory / 'responses/events_subscription.json'

                        
        allowed_values = [
            "productOrderStateChangeEvent",
            "productOrderItemStateChangeEvent",
            "productSpecificProductOrderItemMilestoneEvent",
            "productOrderItemExpectedCompletionDateSet",
            "cancelProductOrderStateChangeEvent",
            "chargeCreateEvent",
            "chargeStateChangeEvent",
            "chargeTimeoutEvent",
            "modifyProductOrderItemRequestedDeliveryDateStateChangeEvent"
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


@router.get('/hub/{id}', response_model=Union[EventSubscription, Error400, Error401, Error403,Error404,  Error500,Error501],
             responses={
                200: common_schema["hub_response_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                501: common_schema["response_501"]
                }
            )

async def retrieves_hub_by_id(
    response: Response,
    id: str = Path(description = "Identifier of the Hub"),
    buyerId: str = Query("", 
                description = "The unique identifier of the organization that is acting \
                as the a Buyer. MUST be specified in the request only when the requester \
                represents more than one Buyer. Reference: MEF 79 (Sn 8.8)"),
    sellerId: str = Query("", 
                description = "The unique identifier of the organization that is acting as\
                the Seller. MUST be specified in the request only when responding entity \
                represents more than one Seller. Reference: MEF 79 (Sn 8.8)")
    ):
    """
    This operation retrieves a hub entity.
    """
    add_headers(response)
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "events_subscription.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            error_404 = {"message": "File not found", "reason": "File not found","referenceError": "https://tools.ietf.org/html/rfc7231", "code": "notFound"}
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=json_compatible_item_data)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            error_404 = { "message": "Record not found", "reason": "Record not found","referenceError": "https://tools.ietf.org/html/rfc7231", "code": "notFound"}
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
            content=json_compatible_item_data)   
        
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

    

@router.delete('/hub/{id}', response_model = Union[Error400, Error401, Error403,Error404,  Error500,Error501],response_class=Response,
             responses={
                204:common_schema["response_delete_204"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404:common_schema["response_404"],
                500: common_schema["response_500"],
                501:common_schema["response_501"]
                }
            )
async def unregister_listener(
       
    id: str=Path(description="The id of the registered listener"),
    buyerId: str = Query("", 
                description="The unique identifier of the organization that is acting \
                as the a Buyer. MUST be specified in the request only when the requester \
                represents more than one Buyer. Reference: MEF 79 (Sn 8.8)"),
    sellerId: str = Query("", 
                description="The unique identifier of the organization that is acting as\
                the Seller. MUST be specified in the request only when responding entity \
                represents more than one Seller. Reference: MEF 79 (Sn 8.8)")
    ):
    """
    Resets the communication endpoint address the service instance must use to deliver information about its health state, execution state, failures and metrics.
    """
    
    try:
        current_directory = Path(__file__).parents[1]
        response_file="events_subscription.json"
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            error_404 = {"message": "File not found", "reason": "File not found","referenceError": "https://tools.ietf.org/html/rfc7231", "code": "notFound"}
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=json_compatible_item_data)
        try:
            with open(file_name,'r') as json_file:
                json_data=json.load(json_file)

        except json.JSONDecodeError as e:
            error_404 = { "message": "Record not found", "reason": "Record not found","referenceError": "https://tools.ietf.org/html/rfc7231", "code": "notFound"}
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
            content=json_compatible_item_data)   
        
        all_keys= json_data.keys()  
              
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
                
            delete_record(id, file_name)

            return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                     
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
