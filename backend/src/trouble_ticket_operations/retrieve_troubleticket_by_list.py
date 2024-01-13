import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from src.validation.sonata.validate_troubleticket import validate_list_troubleticket
from src.common.exceptions import raise_exception
from src.schemas.sonata_schemas.trouble_ticket_schema import TroubleTicket_Find

def retrieve_troubleticket_list(
            externalId, priority, sellerPriority,
            severity,sellerSeverity, ticketType, state,observedImpact,relatedEntityId,relatedEntityType,creationDate_gt,
            creationDate_lt,expectedResolutionDate_gt,expectedResolutionDate_lt,resolutionDate_gt,resolutionDate_lt,buyerId,sellerId, offset, limit
        ):
    try:
        if offset is not None and offset < 0:
            status_msg_code = 400
            message = "'offset' cannot be negative"
            reason = "Invalid offset value"
            reference_error = None
            message_code = "invalidQuery"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if limit is not None and limit < 0:
            status_msg_code = 400
            message = "'limit' cannot be negative"
            reason = "Invalid limit value"
            reference_error = None
            message_code = "invalidQuery"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if offset is None:
            offset = 0
        if limit is None:
            limit = 10

        current_directory = Path(__file__).parents[1]
        response_file = 'trouble_ticket.json'
        file_name = current_directory / 'responses/trouble_ticket.json'
        

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found '{response_file}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(file_name, 'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        extracted_data = []
        for _, troubleticket_info in json_data.items():
            
            json_externalId = troubleticket_info.get("externalId")
            json_priority = troubleticket_info.get("priority")
            json_sellerPriority = troubleticket_info.get("sellerPriority")
            json_severity = troubleticket_info.get("severity")
            json_sellerSeverity = troubleticket_info.get("sellerSeverity")
            json_ticketType = troubleticket_info.get("ticketType")
            json_status = troubleticket_info.get("status")
            json_observedImpact = troubleticket_info.get("observedImpact")
            json_relatedEntityId = troubleticket_info["relatedEntity"][0]["id"]
            json_relatedEntityType = troubleticket_info["relatedEntity"][0]["@referredType"]
            json_creationDate = troubleticket_info.get("creationDate")
            json_expectedResolutionDate = troubleticket_info.get("expectedResolutionDate")
            json_resolutionDate = troubleticket_info.get("resolutionDate")
            json_buyerId = troubleticket_info.get("buyerId")
            json_sellerId = troubleticket_info.get("sellerId")
            

            if (
                (externalId == "" or externalId == json_externalId) and
                (priority == "" or priority == json_priority) and
                (sellerPriority == "" or sellerPriority == json_sellerPriority) and
                (severity == "" or severity == json_severity) and
                (sellerSeverity == "" or sellerSeverity == json_sellerSeverity) and
                (ticketType == "" or ticketType == json_ticketType) and
                (state == "" or state == json_status) and
                (observedImpact == "" or observedImpact == json_observedImpact) and
                (relatedEntityId == "" or relatedEntityId == json_relatedEntityId) and
                (relatedEntityType == "" or relatedEntityType == json_relatedEntityType) and
                (creationDate_gt is None  or (creationDate_gt and creationDate_gt <= json_creationDate)) and
                (creationDate_lt is None  or (creationDate_lt and creationDate_lt >= json_creationDate)) and
                (expectedResolutionDate_gt is None  or (expectedResolutionDate_gt and expectedResolutionDate_gt <= json_expectedResolutionDate)) and
                (expectedResolutionDate_lt is None  or (expectedResolutionDate_lt and expectedResolutionDate_lt >= json_expectedResolutionDate)) and
                (resolutionDate_gt is None  or (resolutionDate_gt and resolutionDate_gt <= json_resolutionDate)) and
                (resolutionDate_lt is None  or (resolutionDate_lt and resolutionDate_lt >= json_resolutionDate)) and
                (buyerId == "" or buyerId == json_buyerId) and
                (sellerId == "" or sellerId == json_sellerId)
            ):
                extracted_info = {
                    "id": troubleticket_info.get("id"),
                    "creationDate": troubleticket_info.get("creationDate"),
                    "description": troubleticket_info.get("description"),
                    "expectedResolutionDate": troubleticket_info.get("expectedResolutionDate"),
                    "externalId": troubleticket_info.get("externalId"),
                    "priority": troubleticket_info.get("priority"),
                    "relatedEntity": troubleticket_info.get("relatedEntity"),
                    "observedImpact": troubleticket_info.get("observedImpact"),
                    "resolutionDate": troubleticket_info.get("resolutionDate"),
                    "sellerPriority": troubleticket_info.get("sellerPriority"),
                    "sellerSeverity": troubleticket_info.get("sellerSeverity"),
                    "severity": troubleticket_info.get("severity"),
                    "status": troubleticket_info.get("status"),
                    "ticketType": troubleticket_info.get("ticketType"),
                }
                extracted_data.append(extracted_info)
        limited_responses = extracted_data[offset: offset + limit]   
        if not limited_responses or not extracted_data:
            status_msg_code = 404
            message = "No matching result found for the given criteria."
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        limited_responses_schema = [TroubleTicket_Find(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        
        validation = validate_list_troubleticket(
            json_data, externalId, priority, sellerPriority,
            severity,sellerSeverity, ticketType, state ,observedImpact,relatedEntityId,relatedEntityType
            
        )

        if validation is True:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8"
            )
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(
                status_msg_code, message, reason, reference_error, message_code, property_path
            )

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
