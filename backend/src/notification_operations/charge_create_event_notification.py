import json
from pathlib import Path
from fastapi import  Response, status
from src.common.exceptions import raise_exception

def charge_create_event(info):
    try:
        cwd = Path(__file__).parents[1]
        charge_filename="charge_response.json"
        charge_response_json = cwd / "responses" / "charge_response.json"

        if not charge_response_json.exists():
            return raise_exception(404, f"File not found '{charge_filename}'", "File not found", None, "notFound", None)
        
        try:
            with open(charge_response_json, "r") as json_file:
                charge_json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(404, "Record not found", "Record not found", None, "notFound", None)

        if info.eventType != "chargeCreateEvent":
            return raise_exception(422, "The eventType must be 'chargeCreateEvent'", "Validation error", None, "invalidValue", "eventType")

        list_of_keys = charge_json_data.keys()
    
        if info.event.id not in list_of_keys :
            return raise_exception(422, f"Invalid Id '{info.event.id}'", "Validation error", None, "invalidValue", "event.Id")

        jsonresult = charge_json_data.get(info.event.id)
        if info.event.sellerId != "" and jsonresult["sellerId"] != info.event.sellerId:
            return raise_exception(422, f"Invalid sellerId '{info.event.sellerId}'", "Validation error", None, "invalidValue", "event.sellerId")
        
        if info.event.href != "" and jsonresult["href"]!=info.event.href:
            return raise_exception(422, f"Invalid href '{info.event.href}'", "Validation error", None, "invalidValue", "event.href")
        
        if info.event.buyerId != "" and jsonresult["buyerId"]!=info.event.buyerId:
            return raise_exception(422, f"Invalid buyerId '{info.event.buyerId}'", "Validation error", None, "invalidValue", "event.buyerId")

        return Response(status_code=status.HTTP_204_NO_CONTENT,media_type="application/json;charset=utf-8")

    except Exception as err:
        return raise_exception(500, str(err), "The server encountered an unexpected condition that prevented it from fulfilling the request", "https://tools.ietf.org/html/rfc7231", "internalError", None)
        