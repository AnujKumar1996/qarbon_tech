
from fastapi import APIRouter, Response, Query
from typing import Union 
from pathlib import Path
from .response_headers import add_headers
from src.schemas.sonata_schemas.geographicaddressmanagement_schema import GeographicAddress , GeographicAddressValidation_Create, GeographicAddressValidation
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404, Error422,
                                                         Error500)
from src.geographical_addressmanagement_operations.retrieve_geographicaddress import retrieve_geographicaddress_id 
from src.geographical_addressmanagement_operations.create_geographicaddress_validation import create_geographicaddress_validation
from src.common.exceptions import raise_exception

router=APIRouter(prefix="/v1/MEF/lsoSonata/geographicAddressManagement"
                 )


@router.get('/geographicAddress/{id}',tags=["GeographicAddress"],
            response_model=Union[GeographicAddress, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["geographic_adddress_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
                
                }
            )
async def retrieves_a_geographicaddress(
    response: Response,
    id: str = Path(description = "Unique (within the Seller domain) identifier for the Appointment."),
    buyerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer. \
            Reference: MEF 79 (Sn 8.8)",
        ),

    sellerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when the responding entity represents more than one Seller. \
            Reference: MEF 79 (Sn 8.8)"
        )
    ):
    """
    This operation retrieves a GeographicAddress entity.
    """
    try:
    
        add_headers(response)
        
        return retrieve_geographicaddress_id(id, buyerId, sellerId)
    
    except Exception as err:
                return raise_exception(status_msg_code=500,
                                    message= str(err), 
                                    reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                    reference_error=None, 
                                    message_code="internalError", 
                                    property_path=None) 
    

@router.post('/geographicAddressValidation',tags=["GeographicAddressValidation"],
            response_model=Union[GeographicAddressValidation, Error400, Error401, Error403, Error422, Error500],
            status_code=200,
            responses={
                200: common_schema["geographic_adddress_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                
                }
            )
async def create_a_geographic_address_validation(
    order: GeographicAddressValidation_Create,
    response:Response,
    buyerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. \
            MUST be specified in the request only when the requester represents more than one Buyer. \
            Reference: MEF 79 (Sn 8.8)",
        ),

    sellerId: str = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. \
            MUST be specified in the request only when the responding entity represents more than one Seller. \
            Reference: MEF 79 (Sn 8.8)"
        )
    ):
    """
    This operation creates a GeographicAddressValidation entity.
    """
   
    try:
        add_headers(response)
        return create_geographicaddress_validation(order, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
      