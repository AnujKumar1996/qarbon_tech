import json
from pathlib import Path
from fastapi import APIRouter, Response, status
from src.common.exceptions import raise_exception
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.common_schemas import CancelProductOrderEvent
from src.schemas.interlude_schemas.error_schemas import (Error404,Error401,Error403, Error408,Error422,Error500)
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime
from src.common.validate_datetime import validate_datetime 

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOrderingManagement/listener",
    tags=["productOrder Notification Listeners"]
    )

@router.post("/cancelProductOrderStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })

def cancel_product_order_state_change_notification_endpoint(info:CancelProductOrderEvent):
    """
    This endpoint is used to receive notifications on Cancel Product Order State Change Event    
    """
    try:
        cwd = Path(__file__).parents[1]
        cancel_sonata_response_file="cancel_sonata_response.json"
        cancel_request_response_fileName = cwd / "responses" / cancel_sonata_response_file
        if not cancel_request_response_fileName.exists():
            status_msg_code = 404
            message = f"File not found '{cancel_sonata_response_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        try:
            with open(cancel_request_response_fileName, "r") as json_file:
                data_json = json.load(json_file)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (empty or invalid JSON)
            status_msg_code = 404
            message = f"Record not found in '{cancel_sonata_response_file}'"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
     
        if info.eventType != "cancelProductOrderStateChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'cancelProductOrderStateChangeEvent'"
            reason = "The requested eventType is invalid"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        event_time = str(info.eventTime)
        isvalid_format = validate_datetime(event_time)
        if not isvalid_format:
            return isvalid_format
        
        validate_event_time = validate_user_startdatetime(event_time)
        if validate_event_time:
            status_msg_code = 422
            message = "The provided eventTime is invalid"
            reason = "The eventTime should be a valid current timestamp"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
     
        
        list_of_cancel_request_keys = data_json.keys()
        if info.event.id not in list_of_cancel_request_keys :
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
                with open(cancel_request_response_fileName, "w") as updated_file:
                    json.dump(data_json, updated_file, indent=4)
                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
            
            else:
                status_msg_code = 422
                message = "The state remains unchanged"
                reason = "The cancellation of the product is still in the same state"
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