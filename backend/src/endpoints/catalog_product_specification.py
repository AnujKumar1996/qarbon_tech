import json
from typing import Optional, Union
from fastapi import APIRouter, Query, Response
from fastapi import APIRouter, Query, Response, status
from src.schemas.sonata_schemas.catalog_productspecification_schema import ProductSpecification_Find
from src.catalog_operations.retrive_productspecification_list import retrive_productspecification_list
from src.catalog_operations.retrive_product_specification_by_id import get_product_specification_by_id
from src.schemas.sonata_schemas.catalog_productspecification_schema import ProductSpecification

from src.common.json_read import common_schema, example_schema
from .response_headers import add_headers
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                          Error500)
from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productCatalog",
    tags=["productSpecification"]
)


@router.get('/productSpecification',
            response_model=Union[ProductSpecification_Find, Error400, Error401, Error403, Error500],
            status_code=200,
            responses={
                200: common_schema["list_response_productSpecification_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                500: common_schema["response_500"],
                }
            )
def lists_or_finds_productspecification_objects(
    
    response: Response,
    name:Optional[str]= Query(
        "",alias="name",
        description="The name of Product Specification (may not be unique)",
    ),
    lifecycleStatus: Optional[str] = Query("",
        description="Lifecycle Status of the Category",
        enum=["active", "endOfSale","endOfSupport","obsolete","onHold","orderable","inTest","rejected"]),
    brand :Optional[str] = Query("",
        alias="brand",
        description="The manufacturer or trademark of the Product Specification if the Seller requires a CPE on the Buyer's premise."),
        
    lastUpdate_gt: Optional[str] = Query(
        None,
        description="The date and time the Product Category was created or most recently updated, greater than.",
        format="data_time",
        alias="lastUpdate.gt"
    ),
    lastUpdate_lt: Optional[str] = Query(
        None,
        description="The date and time the Product Category was created or most recently updated, lesser than.",
        format="data_time",
        alias="lastUpdate.lt"
    ),

    buyerId: Optional[str] = Query("",
        alias="buyerId",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
    ),
    sellerId: Optional[str] = Query("",
        alias="sellerId",
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
        return retrive_productspecification_list(name, lifecycleStatus, brand, lastUpdate_gt, lastUpdate_lt, buyerId , sellerId, offset, limit )
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, 
                               message, reason, 
                               reference_error, 
                               message_code, 
                               property_path)
        
@router.get('/productSpecification/{id}', response_model=Union[ProductSpecification, Error400, Error401, Error403, Error404, Error500],
             status_code=status.HTTP_200_OK,responses={
                200: example_schema["catalog_productSpecification_response_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"]
                }
            )
async def retrieves_a_productspecification_by_id( response: Response,
    id: str ,
    
    buyerId: Optional[str] = Query(
        default="",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
        ),
    sellerId: Optional[str] = Query(
        default="",
        description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the responding entity represents more than one Seller."
        )
    ):
    """
    This operation retrieves a ProductSpecification entity. Attribute selection is enabled for all first level attributes.
    """
    add_headers(response)
    try:
        return get_product_specification_by_id(id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
                                
                                
                               
                              

