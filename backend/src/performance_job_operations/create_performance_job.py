import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.common.create_jsonfile import create_response_json
from src.common.exceptions import raise_exception

from src.schemas.interlude_schemas.performance_job_schemas import PerformanceJob


def create_performance_job(order_data):

    try:
        cwd = Path(__file__).parents[1]
        fileName = cwd / "responses" / "interlude_performance_job.json"

        response_data = order_data
        
        interlude_request_payload_file = cwd / "common" /"interlude_payload.json"

        with open(interlude_request_payload_file) as data:
            interlude_extra_payload = json.load(data)
                    
        response_data["creationDate"] = interlude_extra_payload.get("performance_job_model").get("creationDate")
        response_data["href"] = interlude_extra_payload.get("performance_job_model").get("href")
        response_data["id"] = interlude_extra_payload.get("performance_job_model").get("id")
        response_data["lastModifiedDate"] = interlude_extra_payload.get("performance_job_model").get("lastModifiedDate")
        response_data["state"] = interlude_extra_payload.get("performance_job_model").get("state")
        uniqueid = response_data.get("id")
        
        json_response = response_data.copy()
        json_response["previoustate"] = ""


        json_compatible_item_data = jsonable_encoder(PerformanceJob(**response_data))
        create_response_json(uniqueid, json_compatible_item_data, fileName)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=json_compatible_item_data,
            media_type="application/json;charset=utf-8",
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