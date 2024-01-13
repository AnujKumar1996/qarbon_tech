from typing import Optional, Union
from fastapi import APIRouter, Query, Response
from pathlib import Path
from src.workorder_operations.retrive_workorder_list import retrive_workorder_list
from src.workorder_operations.retrive_workorder_by_id import retrive_workorder_by_id
from src.schemas.sonata_schemas.work_order_schemas import \
    WorkOrder_Find, WorkOrder
from src.common.json_read import common_schema, example_schema
from .response_headers import add_headers
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error422, Error500)
from src.common.exceptions import raise_exception
    
router = APIRouter(
    prefix="/v1/MEF/lsoSonata/workOrderManagement",
    tags=["workorder"]
)



@router.get('/workorder',
            response_model=Union[WorkOrder_Find, Error400, Error401, Error403, Error404, Error422, Error500],
            status_code=200,
            responses={
                200: example_schema["workorder_list_response_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                422: common_schema["response_422"],
                500: common_schema["response_500"],
                }
            )


def lists_or_finds_workorder_objects(
    
    response: Response,
        
    geographicalSiteId: Optional[str] = Query(
        "",
        description="A site identifier that is associated with the Appointment.",
    ),

    geographicalAddressId: Optional[str] = Query(
        "",
        description="An address identifier that is associated with the Appointment.",
    ),

    relatedEntityType: Optional[str] = Query(
        "",
        description="The type of Related Entity (e.g., Trouble Ticket).",
    ),

    relatedEntityId: Optional[str] = Query(
        "",
        description="Identifier of the Related Entity.",
    ),

    state: Optional[str] = Query(
        "",
        description="The state of the WorkOrder.",
        enum=["cancelled", "completed", "inProgress", "open", "planned", "unableToComplete"],
    ),

    appointmentRequired: Optional[bool] = Query(
        None,
        description="Indicates that the Buyer must schedule an Appointment to fulfill the WorkOrder.",
        enum=[True, False]
    ),

    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer. Must be specified in the request only when the requester represents more than one Buyer.",
    ),

    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. Must be specified in the request only when the responding entity represents more than one Seller.",
    ),

    offset: Optional[int] = Query(
        None,
        description="Requested index for the start of resources to be provided in response.",
    ),

    limit: Optional[int] = Query(
        None,
        description="Requested number of resources to be provided in response.",
        format="int32",
    )
    ):
    add_headers(response)
    try:
        return retrive_workorder_list(geographicalSiteId, geographicalAddressId, relatedEntityType, relatedEntityId, state, appointmentRequired, buyerId, sellerId, offset, limit)
        
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

                

@router.get('/workorder/{id}',
            response_model=Union[WorkOrder, Error400, Error401, Error403, Error404, Error422, Error500],
            status_code=200,
            responses={
                200: example_schema["workorder_id_response_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                422: common_schema["response_422"],
                500: common_schema["response_500"],
                }
            )


def retrieves_workorder_by_id(
    response: Response,
    id: str = Path(description = "Unique (within the Seller domain) identifier for the WorkOrder."),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when responding entity represents more than one Seller.",
    ),
    ):
    add_headers(response)
    try:
        return retrive_workorder_by_id(id, buyerId, sellerId)
        
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


