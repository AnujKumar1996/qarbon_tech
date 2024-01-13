from fastapi import APIRouter, Response, Query
from typing import Union ,Optional
from pathlib import Path
from .response_headers import add_headers
from src.schemas.sonata_schemas.geographicsitemanagement_schema import GeographicSite
from src.common.json_read import common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error500,Error422)
from src.geographicsitemanagement_operations.retrieve_geographicsite_by_list import retrieve_geographicsite_list
from src.geographicsitemanagement_operations.retrieve_geographicsite_by_id import retrieve_geographicsite_id
from src.common.exceptions import raise_exception

router=APIRouter(prefix="/v1/MEF/lsoSonata/geographicSiteManagement",
                 tags=["GeographicSite"])


@router.get('/geographicSite/{id}',
            response_model=Union[GeographicSite, Error400, Error401,Error404, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["geographic_site_adddress_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
                
                }
            )
async def retrieves_a_geographicsite_by_id(
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
    This operation retrieves a Geographicsite entity.
    """
    try:
        add_headers(response)
        
        return retrieve_geographicsite_id(id, buyerId, sellerId)
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 


@router.get('/geographicSite',
            response_model=Union[GeographicSite, Error400, Error401,Error404, Error403, Error422, Error500],
            status_code=200,
            responses={
                200: common_schema["geographic_site_adddress_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
            }
            ) 
async def list_or_find_geographicsite_objects(
    response: Response,
    
    companyName: Optional[str] = Query(
        "",
        description="The name of the company that is the administrative authority (e.g. controls access) for this Geographic Site. (For example, the building owner"
    ),
    
    customerName:Optional[str] = Query(
        "",
        description="The name of the company that is the administrative authority for the space within this Geographic Site. ",
        
    ),
    description:Optional[str] = Query(
        "",
        description="A textual description of the Geographic Site",
    ),
    siteType:Optional[str] = Query(
        "",enum=["public", "private"],
        description="This defines whether a Geographic Site is public or private.",
    ),
     
    name:Optional[str] = Query(
        "",
        description="A name commonly used by people to refer to this Geographic Site.",
    ),
    serviceSiteContactName:Optional[str] = Query(
        "",
        description="Identifies the name of the person or organization at the specific site location that is the local contact. This contact will primarily be used for gaining access to the site. Filtering is done on the name of the relatedContactInformation which has the role serviceSiteContactName in the Site record.",
    ),
    geographicAddress_id:Optional[str] = Query(
        "",alias="geographicAddress.id",
        description="Identifier of a geographic address (from the seller). It could be any type of address reference (Fielded, Formatted, GeographicAddressLabel, MEFGeographicPoint)",
    ),
    streetNr:Optional[str] = Query(
        "",
        description="Street Nr of the geographic site",
        
    ),
    streetName:Optional[str] = Query(
        "",
        description="Street Name of the geographic site",
        
    ),
    streetType:Optional[str] = Query(
        "",
        description="Street Type of the geographic site address",
        
    ),
    city:Optional[str] = Query(
        "",
        description="City of the geographic site address",
        
    ),
    postcode:Optional[str] = Query(
        "",
        description="Postcode of the geographic site address",
        
    ),
    country:Optional[str] = Query(
        "",
        description="Country of the geographic site address",
        
    ),

    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer. Must be specified in the request only when the requester represents more than one Buyer.",
    ),

    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. Must be specified in the request only when the responding entity represents more than one Seller.",
    )

    ):
    """
    This operation list or find GeographicSite entities.
    """
    try:        
        add_headers(response)  

        return retrieve_geographicsite_list(country,postcode,city,streetType,streetName,streetNr,geographicAddress_id,serviceSiteContactName,name,siteType,description,customerName,companyName,buyerId, sellerId)

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
 