from fastapi import APIRouter, Response, Query,Path
from typing import Union,Optional
from .response_headers import add_headers
from src.schemas.sonata_schemas.trouble_ticket_schema import TroubleTicket_Create,TroubleTicket,TroubleTicket_Find,TroubleTicket_Update
from src.common.json_read import common_schema,example_schema
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403,Error404,
                                                         Error500, Error422,
                                                         Error409,Error501)
from src.trouble_ticket_operations.create_troubleticket import create_trouble_ticket
from src.trouble_ticket_operations.retrive_trouble_ticket_by_id import retrive_troubleticket_by_id
from src.trouble_ticket_operations.retrieve_troubleticket_by_list import retrieve_troubleticket_list
from src.trouble_ticket_operations.change_inflight_troubleticket import change_inflight_troubleticket
from src.common.exceptions import raise_exception
router=APIRouter(prefix="/v1/MEF/lsoSonata/troubleTicket",
                 tags=["Trouble Ticket and Incident Management"])


@router.post('/troubleTicket',
            response_model=Union[TroubleTicket, Error400, Error401, Error403, Error422, Error500],
            status_code=201,
            responses={
                201: example_schema["response_troubleticket_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                }
            )
async def creates_a_troubleticket(
    order:TroubleTicket_Create,
    response:Response,
     buyerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer."
        ),

    sellerId: Optional[str] = Query(
        default = "",
        description = "The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when responding entity represents more than one Seller."
        )
    ):

    """
    A request initiated by the Buyer to create a Ticket in the Seller's system to report an Issue experienced by the Buyer
    """
    
    add_headers(response)
    try:
        order_dict = order.model_dump(by_alias=True)
        return create_trouble_ticket(order_dict, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 


@router.get(
    '/troubleTicket/{id}',
    response_model=Union[TroubleTicket, Error400, Error401, Error403, Error404, Error422, Error500],
    status_code=200,
    responses={
        200: example_schema["response_productOfferingQualification_201"],
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        404: common_schema["response_404"],
        500: common_schema["response_500"],
    }
)
def retrieves_a_troubleticket_by_id(
    response: Response,
    id: str = Path(
        description="Identifier of the TroubleTicket"
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as a Buyer.\
                    Must be specified in the request only when the requester represents more than one Buyer."
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller.\
                     Must be specified in the request only when the responding entity represents more than one Seller."
    ),
):
    add_headers(response)
    try:
        return retrive_troubleticket_by_id(id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.get('/troubleTicket',
    response_model=Union[TroubleTicket_Find,Error400, Error401, Error403, Error422, Error500],
    status_code=200,
    responses={
        200: example_schema["list_response_troubleticket_200"],
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        500: common_schema["response_500"],
    }
)
def list_or_found_trouble_ticket_objects(
    response: Response,
    externalId: Optional[str] = Query(
        "",
        description="ID given by the consumer and only understandable by him (to facilitate his searches afterward)"
    ),
    priority: Optional[str] = Query(
        "",enum=["low", "medium","high","critical"],
        description="The priority (ITIL) is based on the assessment of the impact and urgency of how quickly the Ticket should be resolved as evaluated by the Buyer. The Priority is used by the Seller to determine the order in which Tickets get resolved across Buyers."
    ),
    sellerPriority: Optional[str] = Query(
        "",enum=["low", "medium","high","critical"],
        description="The priority (ITIL) is based on the assessment of the impact and urgency of how quickly the Ticket should be resolved after evaluation by the Seller of the impact of the Issue on the Buyer."
    ),
    severity: Optional[str] = Query(
        "",enum=["minor", "moderate","significant","extensive"],
        description="The severity or impact (ITIL) of the Ticket as evaluated by the Buyer."
    ),
    sellerSeverity: Optional[str] = Query(
        "",enum=["minor", "moderate","significant","extensive"],
        description="The severity or impact (ITIL) of the Ticket on the Buyer as evaluated by the Seller."
    ),
    ticketType: Optional[str] = Query(
        "",enum=["assistance", "information","installation","maintenance"],
        description="The presumed cause of the Trouble Ticket as evaluated by the Buyer."
    ),
    state: Optional[str] = Query(
        "",enum=["acknowledged", "assessingCancellation","cancelled","closed","inProgress","pending","resolved","reopened"],
        description="The current status of the Trouble Ticket",
        alias="status"
    ),
    observedImpact: Optional[str] = Query(
        "",enum=["degraded", "intermittent","down"],
        description="The type of impact observed by the Buyer."
    ),
    relatedEntityId: Optional[str] = Query(
        "",
        description="ID of a related entity that this ticket is related to and is present in the relatedEntity list"
    ),
    relatedEntityType: Optional[str] = Query(
        "",
        description="Type of a related entity that this ticket is related to and is present in the relatedEntity list"
    ),
    creationDate_gt: Optional[str] = Query(
        None,
        description="The date on which the Trouble Ticket was created - greater than",
        alias="creationDate.gt",
        format="data_time",
    ),
    creationDate_lt: Optional[str] = Query(
        None,
        description="The date on which the Trouble Ticket was created - lower than",
        alias="creationDate.lt",
        format="data_time",
    ),
    expectedResolutionDate_gt: Optional[str] = Query(
        None,
        description="The date provided by the Seller to indicate when the Ticket is expected to be resolved - greater than",
        alias="expectedResolutionDate.gt",
        format="data_time",
    ),
    expectedResolutionDate_lt: Optional[str] = Query(
        None,
        description="The date provided by the Seller to indicate when the Ticket is expected to be resolved - lower than",
        alias="expectedResolutionDate.lt",
        format="data_time",
    ),
    resolutionDate_gt: Optional[str] = Query(
        None,
        description="The date the Ticket status was set to resolved by the Seller - greater than",
        alias="resolutionDate.gt",
        format="data_time",
    ),
    resolutionDate_lt: Optional[str] = Query(
        None,
        description="The date the Ticket status was set to resolved by the Seller - lower than",
        alias="resolutionDate.lt",
        format="data_time",
    ),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Buyer."
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller."
    ),
    offset: Optional[int] = Query(
        None,
        description="Requested index for start of resources to be provided in response"
    ),
    limit: Optional[int] = Query(
        None,
        description="Requested number of resources to be provided in response"
    )
):
    """
    The Buyer requests a list of Trouble Tickets from the Seller based on a set of specified filter criteria. The Seller returns a summarized list of Trouble Tickets
    """
    add_headers(response)
    try:
        return retrieve_troubleticket_list(
            externalId, priority, sellerPriority,
            severity,sellerSeverity, ticketType, state,observedImpact,relatedEntityId,relatedEntityType,creationDate_gt,
            creationDate_lt,expectedResolutionDate_gt,expectedResolutionDate_lt,resolutionDate_gt,resolutionDate_lt,buyerId,sellerId, offset, limit
        )
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.patch('/troubleTicket/{id}',
        response_model=Union[TroubleTicket, Error400, Error401, Error403, Error404, Error500, Error501, Error409],
        responses={
            200: example_schema["response_productOfferingQualification_201"],
            400: common_schema["response_400"],
            401: common_schema["response_401"],
            403: common_schema["response_403"],
            404: common_schema["response_404"],
            409: common_schema["response_409"],
            422: common_schema["response_422"],
            500: common_schema["response_500"]
            
         }
)
def updates_partially_a_troubleticket(
    order: TroubleTicket_Update,
    response: Response,
    id: str,
    buyerId: Optional[str] = Query("", 
                description="The unique identifier of the organization that is acting \
                as the a Buyer. MUST be specified in the request only when the requester \
                represents more than one Buyer. Reference: MEF 79 (Sn 8.8)"),
    
    sellerId: Optional[str] = Query("", 
                description="The unique identifier of the organization that is acting as\
                the Seller. MUST be specified in the request only when responding entity \
                represents more than one Seller. Reference: MEF 79 (Sn 8.8)")
    ):
    """
    A request by the Buyer to patch a Ticket created by the Buyer in the Seller's system
    """
    add_headers(response)
    
    try:
        order_dict = order.model_dump(by_alias=True)
        response = change_inflight_troubleticket(order_dict, id, buyerId, sellerId)
        return response
        
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    