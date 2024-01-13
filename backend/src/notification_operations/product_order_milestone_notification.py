import json
from pathlib import Path
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error404, Error408,
                                                         Error500,Error422)
from src.common.exceptions import raise_exception
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime
from src.common.validate_datetime import validate_datetime 


def product_order_milestone_notification(info):
    """
    This function is used to send notifications on Product Specific Product Order Item Milestone reached.
    """
    try:
       
        cwd = Path(__file__).parents[1]
        sonata_file_name="sonata_response.json"
        sonata_json = cwd / "responses" / "sonata_response.json"
        if not sonata_json.exists():
            return  raise_exception(404, f"File not found '{sonata_file_name}'", "File not found", None, "notFound", None)
        
        try:
            with open(sonata_json, "r") as json_file:
                sonata_json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return  raise_exception(404, "Record not found", "Record not found", None, "notFound", None)

        if info.eventType != "productSpecificProductOrderItemMilestoneEvent":
            return  raise_exception(422, "The eventType must be 'productSpecificProductOrderItemMilestoneEvent'", "The requested eventType is invalid", None, "invalidValue", None)
        
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
     
       
        list_of_keys = sonata_json_data.keys()
    
        if info.event.id not in list_of_keys :
            return  raise_exception(422, f"Invalid Id '{info.event.id}'", "Requested id not found", None, "invalidValue", None)

        jsonresult = sonata_json_data.get(info.event.id)
        if info.event.sellerId != "" and jsonresult["sellerId"] != info.event.sellerId:
            return  raise_exception(422, f"Invalid sellerId '{info.event.sellerId}'", "Requested sellerId not found", None, "invalidValue", None)
        
        if info.event.buyerId != "" and jsonresult["buyerId"]!=info.event.buyerId:
            return  raise_exception(422, f"Invalid buyerId '{info.event.buyerId}'", "Requested buyerId not found", None, "invalidValue", None)

        if info.event.href != "" and jsonresult["href"]!=info.event.href:
            return  raise_exception(422, f"Invalid href '{info.event.href}'", "Requested href not found", None, "invalidValue", None)
        
        if info.event.orderItemId != "":
            product_order_items = jsonresult.get("productOrderItem", [])
            product_ids = [item.get("id") for item in product_order_items]
            if info.event.orderItemId not in product_ids:
                return  raise_exception(422, f"Invalid orderItemId '{info.event.orderItemId}'", "Provide the valid orderItemId", None, "invalidValue", None)
                
        else:
            return  raise_exception(422, "The 'orderItemId' field is required.", "Requested orderItemId not found", None, "missingProperty", None)

        product_order_items = jsonresult.get("productOrderItem", [])
        if info.event.milestoneName != "":
            
            milestone_all_names = []
            for item in product_order_items:
                milestones = item.get("milestone")
                if milestones is not None:
                    for milestone in milestones:
                        milestone_name = milestone.get("name")
                        if milestone_name:
                            milestone_all_names.append(milestone_name)
            
            if info.event.milestoneName in milestone_all_names:
                with open(sonata_json, "w") as updated_file:
                    json.dump(sonata_json_data, updated_file, indent=4)
                    return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")
            else:
                return raise_exception(422, f"Invalid milestoneName '{info.event.milestoneName}'", "Requested milestoneName not found", None, "invalidValue", None)
        else:
            return raise_exception(422, "The 'milestoneName' field is required", "milestoneName must be provided", None, "missingProperty", None)

    except Exception as err:
        return raise_exception(500, str(err), "The server encountered an unexpected condition that prevented it from fulfilling the request", "https://tools.ietf.org/html/rfc7231", "internalError", None)
        