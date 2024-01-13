from typing import Optional, Union
from fastapi.routing import APIRouter
from fastapi import Query, Response, Path
from src.product_offering_qualification_operations.retrive_poq_by_id import retrieve_product_offering_qualification_by_id
from src.product_offering_qualification_operations.retrive_poq_list import retrieve_product_offering_qualification_list
from src.common.json_read import common_schema, example_schema
from src.schemas.sonata_schemas.product_offering_qualification_schema import ProductOfferingQualification_Create, \
                                                                            ProductOfferingQualification, \
                                                                            ProductOfferingQualification_Find
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error422, Error500)
from src.common.exceptions import raise_exception
from src.product_offering_qualification_operations.poq_operation_add import create_product_offering_qualification
from src.product_offering_qualification_operations.poq_operation_delete import disconnect_product_offering_qualification
from src.common.json_read import example_schema, common_schema
from src.schemas.interlude_schemas.error_schemas import (Error400,Error401,Error403,Error422,Error500)
from .response_headers import add_headers
from src.product_offering_qualification_operations.poq_operation_add import create_product_offering_qualification
from src.product_offering_qualification_operations.poq_operation_modify import modify_product_offering_qualification

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productOfferingQualification", 
    tags=["Product Offering Qualification Management"])

@router.get(
    '/productofferingqualification',
    response_model=Union[ProductOfferingQualification_Find,
                         Error400, Error401, Error403, Error404, Error422, Error500],
    status_code=200,
    responses={
        200: example_schema["productofferingqualification_list_response_200"],
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        404: common_schema["response_404"],
        500: common_schema["response_500"],
    }
)
def list_product_offering_qualifications(
    response: Response,
    state: Optional[str] = Query(
        "",
        description="State of the POQ to be retrieved.",
        enum=["acknowledged", "terminatedWithError",
              "inProgress", "done.unableToProvide", "done.ready"]
    ),
    externalId: Optional[str] = Query(
        "",
        description="ID given by the consumer and only understandable by him (to facilitate his searches afterward)."
    ),
    projectId: Optional[str] = Query(
        "",
        description="Identifier of the Buyer project associated with POQ."
    ),
    requestedPOQCompletionDate_gt: Optional[str] = Query(
        None,
        description="POQ expected response date is on or after this date.",
        alias="requestedPOQCompletionDate.gt",
        format="data_time",
    ),
    requestedPOQCompletionDate_lt: Optional[str] = Query(
        None,
        description="POQ expected response date is on or before this date.",
        alias="requestedPOQCompletionDate.lt",
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
        description="Requested index for the start of POQ to be provided in response requested by the client."
    ),
    limit: Optional[int] = Query(
        None,
        description="Requested number of POQ to be provided in response requested by the client."
    )
):
    """
    This function retrieve a list of ProductOfferingQualifications based on a set of criteria
    """
    add_headers(response)
    try:
        return retrieve_product_offering_qualification_list(
            state, externalId, projectId, requestedPOQCompletionDate_gt,
            requestedPOQCompletionDate_lt, buyerId, sellerId, offset, limit
        )
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)



@router.get(
    '/productofferingqualification/{id}',
    response_model=Union[ProductOfferingQualification, Error400, Error401, Error403, Error404, Error422, Error500],
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
def retrieve_product_offering_qualification(
    response: Response,
    id: str = Path(
        description="POQ identifier (matches `ProductOfferingQualification.id`)"
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
        return retrieve_product_offering_qualification_by_id(id, buyerId, sellerId)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

@router.post('/productOfferingQualification',
            response_model=Union[ProductOfferingQualification, Error400, Error401, Error403, Error422, Error500],
            status_code=201,
            responses={
                201: example_schema["response_productOfferingQualification_201"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                422: common_schema["response_422"],
                500: common_schema["response_500"]
                }
            )

async def send_a_request_to_perform_product_offering_qualification(
    order: ProductOfferingQualification_Create,
    response: Response,
    action: str = Query(
        description="Action to be performed on the Product that the Order Item refers to.",
        enum=["add", "modify", "delete"]
    ),
    buyerId: str = Query(
       default="",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer. Reference: MEF 79 (Sn 8.8)",
    ),
    sellerId: str = Query(
        default="",
        description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the responding entity represents more than one Seller. Reference: MEF 79 (Sn 8.8)",
    ),
    ):
    
    """
    A request initiated by the Buyer to determine whether the Seller is able to deliver a product or set of products from among their product offerings, at the Buyer's location(s); or modify a previously purchased product. The Seller also provides estimated time intervals to complete these deliveries. Reference: MEF 79 (Sn 8.4).
    """
    add_headers(response)

    if action == "add":
        try:
            order_dict = order.model_dump(by_alias=True)
            response = create_product_offering_qualification(order_dict, buyerId, sellerId)
            return response
        except Exception as e:
            status_msg_code = 500
            message = str(e)
            reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
            reference_error = None
            message_code = "internalError"
            property_path= None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    elif action == "delete":
        try:
            order_dict = order.model_dump(by_alias=True)
            return disconnect_product_offering_qualification(order_dict, buyerId, sellerId)
        except Exception as e:
            status_msg_code = 500
            message = str(e)
            reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
            reference_error = None
            message_code = "internalError"
            property_path= None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
           
            
    elif action == "modify":
        try:
            order_dict = order.model_dump(by_alias=True)
            return  modify_product_offering_qualification(order_dict, buyerId, sellerId)
       
        except Exception as e:
            status_msg_code = 500
            message = str(e)
            reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
            reference_error = None
            message_code = "internalError"
            property_path= None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    else:
        status_msg_code = 422
        message = "action should be 'add','modify' or 'delete'"
        reason = "Invalid action value"
        reference_error = None
        message_code = "invalidValue"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
 
           