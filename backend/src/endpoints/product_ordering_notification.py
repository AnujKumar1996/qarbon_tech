import json
from pathlib import Path
from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.common_schemas import ProductOrderEvent
from src.notification_operations.product_order_milestone_notification import product_order_milestone_notification
from src.common.exceptions import raise_exception
from src.common.validate_datetime import validate_datetime 
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime


router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOrderingManagement/listener",
    tags=["productOrder Notification Listeners"]
)

@router.post("/productOrderStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
    })

def product_order_state_change_notification_endpoint(info:ProductOrderEvent):
    """
    This endpoint is used to receive notifications on Product Order state change.
    """
    try:
         
        cwd = Path(__file__).parents[1]
        
        sonata_file="sonata_response.json"
        sonata_response_fileName = cwd / "responses" / sonata_file
            
        if not sonata_response_fileName.exists():
            status_msg_code = 404
            message = f"File not found '{sonata_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(sonata_response_fileName, "r") as json_file:
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
        
        if info.eventType != "productOrderStateChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'productOrderStateChangeEvent'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "eventType"
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
        list_of_keys = data_json.keys()
        
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "event.id"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        else:
            jsonresult = data_json[info.event.id]
            if info.event.sellerId != "" and jsonresult["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.sellerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            
            if info.event.buyerId != "" and jsonresult["buyerId"]!=info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.buyerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and  jsonresult["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.href"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            product_order_items = jsonresult.get("productOrderItem", [])
            
            if info.event.milestoneName != "":
                # Extractin all 'name' values from milestone items
                milestone_all_names = []
                for item in product_order_items:
                    milestones = item.get("milestone")
                    if milestones is not None:
                        for milestone in milestones:
                            milestone_name = milestone.get("name")
                            if milestone_name:
                                milestone_all_names.append(milestone_name)
                                
                # Check if the provided milstoname exists in the list of milestone names
                if info.event.milestoneName not in milestone_all_names:
                    status_msg_code = 422
                    message = f"Invalid milestoneName '{info.event.milestoneName}'"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = "event.milestoneName"
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            if info.event.orderItemId != "":
                product_order_items = jsonresult.get("productOrderItem", [])
                product_ids = [item.get("id") for item in product_order_items]
                if info.event.orderItemId not in product_ids:
                    status_msg_code = 422
                    message = f"Invalid orderItemId '{info.event.orderItemId}'"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = "event.orderItemId"
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
            current_state = jsonresult.get("state")
            previous_state = jsonresult.get("previoustate")
            
            if current_state != previous_state:
                jsonresult["previoustate"] = current_state
                
                with open(sonata_response_fileName, "w") as updated_file:
                    json.dump(data_json, updated_file, indent=4)
                    
                return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
            
            else:
                status_msg_code = 422
                message = "The state remains unchanged"
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


@router.post("/productOrderItemStateChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })

def product_order_item_change_notification_endpoint(info:ProductOrderEvent):
    """
    This endpoint is used to receive notifications on Product Order Item state change.
    """
    try:

        cwd = Path(__file__).parents[1]
        sonata_file="sonata_response.json"
        sonata_response_fileName = cwd / "responses" / sonata_file
        
        if not sonata_response_fileName.exists():
            status_msg_code = 404
            message = f"File not found: '{sonata_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
                with open(sonata_response_fileName, "r") as json_file:
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

        list_of_keys = data_json.keys()
        
        if info.eventType != "productOrderItemStateChangeEvent":
            status_msg_code = 422
            message = "The eventType must be 'productOrderItemStateChangeEvent'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "eventType"
                
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if info.event.id not in list_of_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = "event.id"
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        else:
            jsonresult = data_json[info.event.id]
            if info.event.sellerId != "" and jsonresult["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.sellerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.buyerId != "" and jsonresult["buyerId"]!=info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.buyerId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href != "" and jsonresult["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.href"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            product_order_items = jsonresult.get("productOrderItem", [])
            
            if info.event.milestoneName != "":
                # Extractin all 'name' values from milestone items
                milestone_all_names = []
                for item in product_order_items:
                    milestones = item.get("milestone")
                    if milestones is not None:
                        for milestone in milestones:
                            milestone_name = milestone.get("name")
                            if milestone_name:
                                milestone_all_names.append(milestone_name)
                # Check if the provided milstoname exists in the list of milestone names
                if info.event.milestoneName not in milestone_all_names:
                    status_msg_code = 422
                    message = f"Invalid milestoneName '{info.event.milestoneName}'"
                    reason = "Validation error"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = "event.milestoneName"
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            result=False    
            if info.event.orderItemId != "":
                for product_index,item in enumerate(product_order_items):
                    if info.event.orderItemId == item.get("id"):
                        product_status=item.get("state")
                        product_previoustate=item.get("previoustate")
                        result=True
                        index=product_index
                        break
            else:
                status_msg_code = 422
                message = "'event.orderItemId' must be provided"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.orderItemId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                       
            if not result:
                status_msg_code = 422
                message = f"Invalid orderItemId '{info.event.orderItemId}'"
                reason = "Validation error"
                reference_error = None
                message_code = "invalidValue"
                property_path = "event.orderItemId"
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            else:
                current_state = product_status
                previous_state = product_previoustate
                
                if current_state != previous_state:
                    jsonresult["productOrderItem"][index]["previoustate"] = current_state
                    
                    with open(sonata_response_fileName, "w") as updated_file:
                        json.dump(data_json, updated_file, indent=4)
                        #Successful response
                        return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                    
                else:
                    status_msg_code = 422
                    message = "The state remains unchanged"
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
  

@router.post("/productOrderItemExpectedCompletionDateSet",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
        responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })

def product_order_item_expected_completion_date_set_notification_endpoint(info:ProductOrderEvent):
    """
    This endpoint is used to receive notifications on Product Order Item Expected Completion Date Set.
    """
    try:
        cwd = Path(__file__).parents[1]
        sonata_file="sonata_response.json"
        sonata_response_fileName = cwd / "responses" / "sonata_response.json"
        
        if not sonata_response_fileName.exists():
            status_msg_code = 404
            message = f"File not found '{sonata_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(sonata_response_fileName, "r") as json_file:
                data_json = json.load(json_file)
        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if info.eventType != "productOrderItemExpectedCompletionDateSet":
            status_msg_code = 422
            message = "The eventType must be 'productOrderItemExpectedCompletionDateSet'"
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
        
        list_of_sonata_keys = data_json.keys()

        if info.event.id not in list_of_sonata_keys :
            status_msg_code = 422
            message = f"Invalid id '{info.event.id}'"
            reason = "Requested id not found"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        else:
            jsonresult = data_json[info.event.id]
            if info.event.sellerId !=  "" and jsonresult["sellerId"] != info.event.sellerId:
                status_msg_code = 422
                message = f"Invalid sellerId '{info.event.sellerId}'"
                reason = "Requested sellerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            if info.event.buyerId !=  "" and jsonresult["buyerId"] != info.event.buyerId:
                status_msg_code = 422
                message = f"Invalid buyerId '{info.event.buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if info.event.href !=  "" and jsonresult["href"]!=info.event.href:
                status_msg_code = 422
                message = f"Invalid href '{info.event.href}'"
                reason = "Requested href not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
            product_order_items = jsonresult.get("productOrderItem", [])
            
            if info.event.milestoneName !=  "":
                # Extractin all 'name' values from milestone items
                milestone_all_names = []
                for item in product_order_items:
                    milestones = item.get("milestone")
                    if milestones is not None:
                        for milestone in milestones:
                            milestone_name = milestone.get("name")
                            if milestone_name:
                                milestone_all_names.append(milestone_name)
                # Check if the provided milstoname exists in the list of milestone names
                if info.event.milestoneName not in milestone_all_names:
                    status_msg_code = 422
                    message = f"Invalid milestoneName '{info.event.milestoneName}'"
                    reason = "Requested milestoneName not found"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            result = False    
            expectedCompletionDate = None
            if info.event.orderItemId != "":
                for item in product_order_items:
                    if info.event.orderItemId == item.get("id"):
                        if item.get("expectedCompletionDate") is not None:
                            expectedCompletionDate=item.get("expectedCompletionDate")
                        result = True
                        break
            else:
                status_msg_code = 422
                message = "The 'orderItemId' filed is required"
                reason = "Requested orderItemId not found"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if not result:
                status_msg_code = 422
                message = f"Invalid orderItemId '{info.event.orderItemId}'"
                reason = "Provide the valid orderItemId"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            else:
                if expectedCompletionDate is not None:
                        
                    return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
                    
                else:
                    status_msg_code = 422
                    message = "The seller has not specified a completion date"
                    reason = "Missing completion date information"
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
                        
@router.post("/productSpecificProductOrderItemMilestoneEvent", status_code = status.HTTP_204_NO_CONTENT, response_class = Response,
              responses={
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    })
def product_specific_product_order_item_milestone_notification_endpoint(info:ProductOrderEvent):
    """
    This endpoint is used to receive notifications on Product Specific Product Order Item Milestone reached.
    """
    try:
       return product_order_milestone_notification(info)
    except Exception as err:
        return raise_exception(500, str(err), "The server encountered an unexpected condition that prevented it from fulfilling the request", "https://tools.ietf.org/html/rfc7231", "internalError", None) 
