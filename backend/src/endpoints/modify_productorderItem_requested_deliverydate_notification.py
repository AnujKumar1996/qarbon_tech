import json
from pathlib import Path
from fastapi import APIRouter, Response, status
from src.common.exceptions import raise_exception
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.common_schemas import ModifyProductOrderItemRequestedDeliveryDateEvent
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime
from src.common.validate_datetime import validate_datetime 

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOrderingManagement/listener",
    tags=["productOrder Notification Listeners"]
)

@router.post("/modifyProductOrderItemRequestedDeliveryDateStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })

def modify_product_order_item_requested_delivery_date_state_change_notification_endpoint(info:ModifyProductOrderItemRequestedDeliveryDateEvent):
    """
    This endpoint is used to receive notifications on Modify Product Order Item Requested Delivery Date State Change Event.
    """
    try:
        cwd = Path(__file__).parents[1]
        modify_request_file="modify_request_response.json"
        modify_reques_response_fileName = cwd / "responses" / modify_request_file
        
        if not modify_reques_response_fileName.exists():
            status_msg_code = 404
            message = f"File not found: {modify_request_file}"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(modify_reques_response_fileName, "r") as json_file:
                data_json = json.load(json_file)
                
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (empty or invalid JSON)
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        if info.eventType != "modifyProductOrderItemRequestedDeliveryDateStateChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'modifyProductOrderItemRequestedDeliveryDateStateChangeEvent'"
            reason = "The requested eventType is invalid"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if isvalid_format:
            return isvalid_format
        
        validate_event_time = validate_user_startdatetime(event_time)
        if not validate_event_time:
            status_msg_code = 422
            message = "The provided eventTime is invalid"
            reason = "The eventTime should be a valid current timestamp"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
     
        list_of_modify_request_keys = data_json.keys()
    
        if info.event.id not in list_of_modify_request_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        else:
            jsonresult = data_json[info.event.id]
            if info.event.sellerId != "" and jsonresult["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.buyerId != "" and jsonresult["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            if info.event.href != "" and jsonresult["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            current_state = jsonresult.get("state")
            previous_state = jsonresult.get("previoustate")
            
            if current_state != previous_state:
                jsonresult["previoustate"] = current_state
                with open(modify_reques_response_fileName, "w") as updated_file:
                    json.dump(data_json, updated_file, indent=4)
                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
            
            else:
                status_msg_code = 422
                message = "The state remains unchanged"
                reason = "The state remains the same"
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


            
                                  
