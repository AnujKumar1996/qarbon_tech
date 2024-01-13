import json
from pathlib import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.geographicsitemanagement_schema import GeographicSite
from src.common.exceptions import raise_exception

def retrieve_geographicsite_id(id, buyerId, sellerId):
    """
    Retrieve geographic site information based on the provided site ID, buyer ID, and seller ID.

    Parameters:
    - id (str): The ID of the geographic site.
    - buyerId (str): The buyer ID to validate against the retrieved site information.
    - sellerId (str): The seller ID to validate against the retrieved site information.

    Returns:
    - JSONResponse: A JSON response containing the geographic site information if successful, or an error response if not found or encountering an unexpected condition.

    Raises:
    - HTTPException: Raises an HTTPException with appropriate status code and error details.

    Description:
    - This function attempts to retrieve geographic site information from a JSON file based on the provided site ID.
    - It checks if the file exists and then loads the JSON data.
    - Validates the buyer ID and seller ID against the retrieved site information.
    - If successful, it converts the site information to JSON format and returns a JSONResponse.
    - If the site ID is not found or validation fails, it raises an HTTPException with a corresponding error message.
    - If any unexpected exception occurs during the process, it raises an HTTPException with a 500 status code and an internal error message.

    """
    try:
        current_directory = Path(__file__).parents[1]
        response_file = "geographicsitemanagement_geographicsite.json"
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
        
        if id in all_keys and json_data.get(id).get('id') == id:
            
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
            
            
            json_compatible_item_data=jsonable_encoder(GeographicSite(**order_info))
        
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
