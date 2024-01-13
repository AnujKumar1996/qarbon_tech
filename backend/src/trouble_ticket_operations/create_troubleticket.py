import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.common.create_jsonfile import create_response_json
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.trouble_ticket_schema import TroubleTicket
from src.common.validate_datetime import validate_datetime
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime, validate_lesser_than_current_datetime
from datetime import datetime


def create_trouble_ticket(order_data, buyerId, sellerId):
    try:
        for items in order_data.get("relatedContactInformation"):
            if items.get("role") != "reporterContact" :
                status_msg_code = 422
                message = "The Buyer's request must specify a relatedContactInformation item with a role set to reporterContact"
                reason = "The request from the buyer must include a relatedContactInformation item, and this item must have a role designated as reporterContact"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if order_data.get("attachment") is not None:
            for item in order_data.get("attachment"):
                if not item.get("url")  and (not item.get("content") or not item.get("mimeType")):
                    status_msg_code = 422
                    message = "The buyer must either provide attachment.url or (attachment.content and attachment.mimeType)"
                    reason = "Specify either attachment.url or provide both attachment.content and attachment.mimeType"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
                if item.get("source") != "buyer" :
                    status_msg_code = 422
                    message = "The Buyer must set the respective source=buyer"
                    reason = "The Buyer is required to set the source attribute to source=buyer"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                    
        if order_data.get("note") is not None:
            for items in order_data.get("note"):
                if items.get("source") != "buyer" :
                    status_msg_code = 422
                    message = "The Buyer must set the source=buyer"
                    reason = "The Buyer is required to set the source attribute to source=buyer"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if order_data.get("relatedIssue") is not None:
            for item in order_data.get("relatedIssue"):
                if item.get("source") != "buyer" :
                    status_msg_code = 422
                    message = "The Buyer must set the source=buyer"
                    reason = "The Buyer is required to set the source attribute to source=buyer"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if order_data['attachment'] is not None:
            for item in order_data['attachment']:
                attachment_creationdate=item.get('creationDate')
                isvalid_format = validate_datetime(str(attachment_creationdate))
                if isvalid_format:
                    return isvalid_format
                validate_event_time = validate_user_startdatetime(str(attachment_creationdate))
                if not validate_event_time:
                    status_msg_code = 422
                    message = "The 'creationDate' must be current date"
                    reason = "The 'creationDate' should be a valid current timestamp"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                        
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                current_time = datetime.utcnow()
                formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                item["creationDate"] = formatted_time   
                    
        if order_data['relatedIssue'] is not None:
            for item in order_data['relatedIssue']:
                relatedissue_creationdate=item.get('creationDate')
                isvalid_format = validate_datetime(str(relatedissue_creationdate))
                if isvalid_format:
                    return isvalid_format
                validate_event_time = validate_user_startdatetime(str(relatedissue_creationdate))
                if not validate_event_time:
                    status_msg_code = 422
                    message = "The 'creationDate' must be current date"
                    reason = "The 'creationDate' should be a valid current timestamp"
                    reference_error = None
                    message_code = "invalidValue"
                    property_path = None
                        
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                current_time = datetime.utcnow()
                formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                item["creationDate"] = formatted_time  
                  
        if order_data['issueStartDate'] is not None:
            issuestartdate=order_data.get("issueStartDate")
            isvalid_format = validate_datetime(str(issuestartdate))
            if isvalid_format:
                return isvalid_format
            current_time = datetime.utcnow()
            formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            validate_event_time = validate_lesser_than_current_datetime(str(issuestartdate))
            if not validate_event_time:
                status_msg_code = 422
                message = "The 'issueStartDate' must be valid date"
                reason = "The 'issueStartDate' must not be greater than current date"
                reference_error = None
                message_code = "invalidValue"
                property_path = None
                    
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                            
                
        current_directory = Path(__file__).parents[1]
        file_name = current_directory / 'responses/trouble_ticket.json'
        
        payload_file_name = current_directory / 'common/sonata_payloads.json'
        with open(payload_file_name, "r") as json_file:
            json_payload = json.load(json_file)

        order_data["id"]  =  json_payload.get("troubleTicket_payload").get("id") 
        order_data["status"] = json_payload.get("troubleTicket_payload").get("status")
        order_data["creationDate"] = json_payload.get("troubleTicket_payload").get("creationDate")
        order_data["sellerPriority"] = json_payload.get("troubleTicket_payload").get("sellerPriority")
        order_data["sellerSeverity"] = json_payload.get("troubleTicket_payload").get("sellerSeverity")
        order_data["resolutionDate"] = json_payload.get("troubleTicket_payload").get("resolutionDate")
        order_data["expectedResolutionDate"] = json_payload.get("troubleTicket_payload").get("expectedResolutionDate")

        response_data = jsonable_encoder(TroubleTicket(**order_data))
        json_response = response_data.copy()
        json_response["buyerId"] = buyerId
        json_response["sellerId"] = sellerId
        json_response["previoustate"] = order_data["status"]
        
        
        create_response_json(order_data["id"], json_response, file_name)   
                
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=response_data,
                            media_type="application/json;charset=utf-8"
                            )
    except ValidationError as e:
        status_msg_code = 422
        message = str(e)
        reason = "Validation error"
        reference_error = None
        message_code = "invalidValue"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
    except Exception as e:
        status_msg_code = 500
        message = str(e)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path= None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        
        
            
                
            
        

                
        
        