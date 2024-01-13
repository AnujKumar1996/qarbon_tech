from pathlib import Path
from typing import Union, Optional
from fastapi import APIRouter, Query, Response
from src.common.exceptions import raise_exception
from src.common.json_read import common_schema, example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error422, Error500 )
from src.schemas.sonata_schemas.product_catalog_productoffering_schemas import ProductOffering, ProductOffering_Find
from .response_headers import add_headers
from src.catalog_operations.retrive_productoffering import retrive_productoffering
from src.catalog_operations.retrive_productoffering_list import retrive_productoffering_list
 
router = APIRouter( prefix="/v1/MEF/lsoSonata/productCatalog",tags=["productOffering"])


@router.get('/productOffering',
            response_model=Union[ProductOffering_Find, Error400, Error401, Error403, Error404, Error422, Error500],
            status_code=200,
            responses={
                200: example_schema["list_response_offering_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                403: common_schema["response_404"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                }
            )

def lists_or_finds_Offering_objects(
    response: Response,
    name: Optional[str] = Query(
        "",
        description="The commercial name of the Product Offering.",
    ),
    lastUpdate_gt: Optional[str] = Query(
        None,
        description="The date and time the Product Offering was created or most recently updated, greater than.",
        format="data_time",
        alias="lastUpdate.gt"
    ),
    lastUpdate_lt: Optional[str] = Query(
        None,
        description="The date and time the Product Offering was created or most recently updated, lesser than.",
        format="data_time",
        alias="lastUpdate.lt"
    ),
    lifecycleStatus: Optional[str] = Query(
        "",
        description="Lifecycle Status of the Product Offering",
        enum=["active", "endOfSale", "endOfSupport", "obsolete", "onHold", "orderable", "pilotBeta", "rejected"]
    ),
    agreement: Optional[str] = Query(
        "",
        description='''The name of the Seller's offer arrangement (such as a framework agreement).
            **Note:** The list of allowable values for agreements should be negotiated between the Buyer and the Seller,
                      during the integration phase. Ultimately it will be the enumerated set of values (it's problematic
                      to define the enumerated values globally for any operator).''',
    ),
    channel: Optional[str] = Query(
        "",
        description='''The names of the sales channel through which the Product Offering is made available to the Buyer to order.
            **Note:** The list of allowable values for selling channels should be negotiated between the Buyer 
                      and the Seller, during the integration phase. 
                      Ultimately it will be the enumerated set of values (it's problematic to define 
                      the enumerated values globally for any operator).''',
    ),
    marketSegment: Optional[str] = Query(
        "",
        description='''The names of the market segments  targeted for the Product Offering.
            **Note:** The list of allowable values for selling market segments should be negotiated between the Buyer 
                      and the Seller, during the integration phase. 
                      Ultimately it will be the enumerated set of values (it's problematic to define 
                      the enumerated values globally for any operator).''',
    ),
    region_country: Optional[str] = Query(
        "",
        description="Country where the products are offered by the Seller to potential Buyers.",
        alias="region.country"
    ),
    category_id: Optional[str] = Query(
        "",
        description='''Reference Identifier of the Category that Product Offering is the direct 
        or transitive member of. Direct member - there is a direct relation between Category and Product Offering.
        Transitive member - there is a relation between one of the sub-categories and Product Offering.''',
        alias="category.id"
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the responding entity represents more than one Seller.",
    ),
    offset: Optional[int] = Query(
        None,
        description="Requested index for start of item to be provided in response requested by the client. Note that the index starts with '0'.",
        alias="offset",
        format="int32",
    ),
    limit: Optional[int] = Query(
        None,
        description="Requested number of items to be provided in response requested by client",
        alias="limit",
        format="int32",),
):
    add_headers(response)
    try:
        return retrive_productoffering_list(name, lastUpdate_gt, lastUpdate_lt, lifecycleStatus, agreement ,
                        channel, marketSegment, region_country, category_id, buyerId, sellerId, offset, limit) 
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)



@router.get('/productOffering/{id}', response_model=Union[ProductOffering, Error400, Error401, Error403,  Error500,Error404],
             responses={
                200: common_schema["productOffering_git_by_Id"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_404"],
                500: common_schema["response_500"],
                
                }
            )

async def retrieves_productoffering_by_id(
     
    response: Response,
    id: str = Path(default = None, description = "Identifier of the productOffering"),
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
    This operation retrieves a ProductOffering entity. Attribute selection is enabled for all first level attributes.
    """
    add_headers(response)
    try:
        
        return retrive_productoffering(id, buyerId, sellerId)
    
    except Exception as err:
           return raise_exception(status_msg_code=500,
                                  message= str(err), 
                                  reason="The server encountered an unexpected condition that prevented it from fulfilling the request", 
                                  reference_error=None, 
                                  message_code="internalError", 
                                  property_path=None) 

