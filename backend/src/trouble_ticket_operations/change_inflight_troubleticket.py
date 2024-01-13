import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.trouble_ticket_schema import TroubleTicket
from src.common.validate_datetime import validate_datetime
from src.validation.sonata.validate_create_appointment import validate_user_startdatetime, validate_lesser_than_current_datetime
from datetime import datetime

def change_inflight_troubleticket(order_data,id, buyerId, sellerId):
    
    try:

        if order_data.get('externalId') != "" or order_data.get('priority') is not None or order_data.get('severity') is not None or order_data.get('issueStartDate') is not None or order_data.get('observedImpact') is not None or order_data.get('attachment') is not None or order_data.get('note') is not None or order_data.get('relatedContactInformation') is not None or order_data.get('relatedIssue') is not None:
            
            current_directory = Path(__file__).parents[1]
            response_file = "trouble_ticket.json"
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
                    troubleticket_json_data = json.load(json_file)

            except json.JSONDecodeError as e:
                return raise_exception(status_msg_code=404, 
                                        message="Record not found", 
                                        reason="Record not found", 
                                        reference_error=None, 
                                        message_code="notFound", 
                                        property_path=None)        
            all_keys = troubleticket_json_data.keys()  

            if id in all_keys:
                
                troubleticket_jsondata_of_particular_id = troubleticket_json_data[id]
                
                if buyerId != "" and buyerId != troubleticket_jsondata_of_particular_id.get("buyerId"): 
                            
                    status_msg_code = 404
                    message = f"Invalid buyerId '{buyerId}'"
                    reason = "Requested buyerId not found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                if sellerId != "" and  sellerId != troubleticket_jsondata_of_particular_id.get("sellerId"): 

                    status_msg_code = 404
                    message = f"Invalid sellerId '{sellerId}'"
                    reason = "Requested sellerId not Found"
                    reference_error = None
                    message_code = "notFound"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                
                current_status=troubleticket_jsondata_of_particular_id.get("status")
                if current_status == "assessingCancellation" or current_status == "cancelled" or current_status == "closed":
                    
                    status_msg_code = 422
                    message = f"The troubleTicket status is in {current_status}"
                    reason = "Updating the trouble ticket is not allowed if its state is 'assessingCancellation,' 'cancelled,' or 'closed"
                    reference_error = None
                    message_code = "missingProperty"
                    property_path = None
                    
                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                if order_data.get("attachment") is not None:
                    for item in order_data.get("attachment"):
                        if not item.get("url")  and (not item.get("content") or not item.get("mimeType")):
                            status_msg_code = 422
                            message = "The buyer must either provide attachment url or (attachment content and attachment mimeType)"
                            reason = "Specify either attachment url or provide both attachment content and attachment mimeType"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                       
                        if item.get("source") != "buyer":
                            status_msg_code = 422
                            message = "The Buyer must set the 'source' attribute value to 'buyer' while adding to 'attachment'"
                            reason = "The Buyer needs to make sure that the 'source' attribute is set to 'buyer'"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
              
                if order_data.get("note") is not None:
                    for item in order_data.get("note"):
                        if item.get("source") != "buyer":
                            status_msg_code = 422
                            message = "The Buyer must set the 'source' attribute value to 'buyer' while adding to 'note'"
                            reason = "The Buyer needs to make sure that the 'source' attribute is set to 'buyer'"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
              
                if order_data.get("relatedIssue") is not None:
                    for item in order_data.get("relatedIssue"):
                        if item.get("source") != "buyer":
                            status_msg_code = 422
                            message = "The Buyer must set the 'source' attribute value to 'buyer' while adding to 'relatedIssue'"
                            reason = "The Buyer needs to make sure that the 'source' attribute is set to 'buyer'"
                            reference_error = None
                            message_code = "invalidValue"
                            property_path = None
                            
                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
              
                if (
                    order_data.get('priority') is not None or
                    order_data.get('severity') is not None or
                    order_data.get('issueStartDate') is not None or
                    order_data.get('relatedIssue') is not None) and order_data.get('note') is None:
                   
                    status_msg_code = 422
                    message = "The Buyer must add a 'note' to a troubleTicket when any of the following attributes are patched: 'priority', 'severity', 'issueStartDate', 'relatedIssue'"
                    reason = "If the Buyer updates attributes such as 'priority', 'severity', 'issueStartDate', or 'relatedIssue' they should include a 'note' in the trouble ticket"
                    reference_error = None
                    message_code = "missingProperty"
                    property_path = None

                    return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                
                if order_data['relatedContactInformation'] is not None:
                    for item in order_data['relatedContactInformation']:  
                        if item.get("role") != "buyerContactInformation":
                            status_msg_code = 422
                            message = "The Buyer's request must specify a 'relatedContactInformation' item with a role set to 'buyerContactInformation'"
                            reason = "The request from the buyer must include a 'relatedContactInformation' item, and this item must have a role designated as 'buyerContactInformation'"
                            reference_error = None
                            message_code = "missingProperty"
                            property_path = None

                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

            
                attachment_creationdate=None
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
                        
                
                if order_data['externalId'] is not None:
                    troubleticket_jsondata_of_particular_id['externalId']= order_data.get("externalId")
                    
                if order_data['priority'] is not None:
                    troubleticket_jsondata_of_particular_id['priority']= order_data.get("priority")
                    
                if order_data['severity'] is not None:
                    troubleticket_jsondata_of_particular_id['severity']= order_data.get("severity")
                    
                if order_data['issueStartDate'] is not None:
                    troubleticket_jsondata_of_particular_id['issueStartDate']= order_data.get("issueStartDate")
                    
                if order_data['observedImpact'] is not None:
                    troubleticket_jsondata_of_particular_id['observedImpact']= order_data.get("observedImpact")
                    
                if order_data['note'] is not None:  
                    if troubleticket_jsondata_of_particular_id.get('note') is not None:
                            
                        json_res_note_data = troubleticket_jsondata_of_particular_id['note']
                        json_res_note_data.extend(order_data['note'])
                        troubleticket_jsondata_of_particular_id['note'] = json_res_note_data
                    else:
                        troubleticket_jsondata_of_particular_id['note'] = order_data['note'] 
                        
                if order_data['attachment'] is not None: 
                    
                    if troubleticket_jsondata_of_particular_id.get('attachment') is not None:
                        json_res_attachment_data = troubleticket_jsondata_of_particular_id['attachment']
                        json_res_attachment_data.extend(order_data['attachment'])
                        troubleticket_jsondata_of_particular_id['attachment'] = json_res_attachment_data
                    else:
                        troubleticket_jsondata_of_particular_id['attachment'] = order_data['attachment'] 
                       
                if order_data['relatedContactInformation'] is not None: 
                    
                    if troubleticket_jsondata_of_particular_id.get('relatedContactInformation') is not None:
                        jsondata_of_relatedContactInformation = troubleticket_jsondata_of_particular_id['relatedContactInformation']
                        jsondata_of_relatedContactInformation.extend(order_data['relatedContactInformation'])
                        troubleticket_jsondata_of_particular_id['relatedContactInformation'] = jsondata_of_relatedContactInformation
                    else:
                        troubleticket_jsondata_of_particular_id['relatedContactInformation'] = order_data['relatedContactInformation']  
                        
                if order_data['relatedIssue'] is not None: 
                    
                    if troubleticket_jsondata_of_particular_id.get('relatedIssue') is not None:
                        jsondata_of_relatedIssue = troubleticket_jsondata_of_particular_id['relatedIssue']
                        jsondata_of_relatedIssue.extend(order_data['relatedIssue'])
                        troubleticket_jsondata_of_particular_id['relatedIssue'] = jsondata_of_relatedIssue
                    else:
                        troubleticket_jsondata_of_particular_id['relatedIssue'] = order_data['relatedContactInformation']  
                
                if troubleticket_jsondata_of_particular_id.get("status") == "pending":
                    troubleticket_jsondata_of_particular_id["status"] = "inProgress"
                
                 
                response_data = jsonable_encoder(TroubleTicket(**troubleticket_jsondata_of_particular_id))
                response_data["buyerId"] = troubleticket_jsondata_of_particular_id.get("buyerId")
                response_data["sellerId"] = troubleticket_jsondata_of_particular_id.get("sellerId")
                response_data["previoustate"] = troubleticket_jsondata_of_particular_id.get("previoustate")
                create_response_json(id, response_data, file_name)

                return JSONResponse(status_code=status.HTTP_200_OK,
                                                    content=response_data,
                                                    media_type="application/json;charset=utf-8"
                                                    )
                
            else:
                return raise_exception(status_msg_code=404,
                                    message=f"Invalid id '{id}'", 
                                    reason="Requested id not found",
                                    reference_error=None,
                                    message_code="notFound",
                                    property_path=None)    
    
        else:
            status_msg_code = 422
            message = "At least one of the following attributes is required: 'attachment', 'note', 'relatedContactInformation', 'externalId', 'issueStartDate', 'observedImpact', 'priority', 'relatedIssue', 'severity'"
            reason="Required attributes are missing."
            reference_error = None
            message_code = "missingProperty"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
      
    except Exception as err:
            return raise_exception(status_msg_code=500,
                                   message= str(err), 
                                   reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                   reference_error=None, 
                                   message_code="internalError", 
                                   property_path=None) 
        