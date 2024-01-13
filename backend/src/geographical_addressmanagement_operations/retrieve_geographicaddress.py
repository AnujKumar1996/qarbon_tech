import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.geographicaddressmanagement_schema import GeographicAddress
from src.common.exceptions import raise_exception

def retrieve_geographicaddress_id(id, buyerId, sellerId):
    
    """
    Retrieve geographic address information by ID.

    Parameters:
    - id (str): Unique identifier for the geographic address.
    - buyerId (str): Optional parameter for filtering by buyer ID.
    - sellerId (str): Optional parameter for filtering by seller ID.

    Returns:
    - JSONResponse: A JSON response containing geographic address information.

    Raises:
    - HTTPException: Raised for various error scenarios, including file not found,
      record not found, invalid buyerId, invalid sellerId, and internal server error.
    """
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "geographicaddress_management_geographicaddress.json"
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
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)        
        all_keys = json_data.keys()  
        if id in all_keys :
            
            order_info = json_data.get(id)
            
            if buyerId != "" and buyerId != order_info.get("buyerId"): 
                        
                status_msg_code = 404
                message = f"Invalid buyerId '{buyerId}'"
                reason = "Requested buyerId not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            if sellerId != "" and  sellerId != order_info.get("sellerId"): 

                status_msg_code = 404
                message = f"Invalid sellerId '{sellerId}'"
                reason = "Requested sellerId not Found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
            
            json_compatible_item_data=jsonable_encoder(GeographicAddress(**order_info))
            return JSONResponse(status_code=status.HTTP_200_OK,
                            content=json_compatible_item_data,
                            media_type="application/json;charset=utf-8")
            
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
