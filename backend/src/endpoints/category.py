import json
from typing import Optional, Union
from fastapi import APIRouter, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from src.schemas.sonata_schemas.category_schemas import \
    ProductCategory
from src.validation.sonata.validating_sellerId_buyerId import check_seller_id, check_buyer_id
from src.common.validate_datetime import validate_datetime_format
from src.validation.sonata.validate_category import validate_list_category,validate_category
from src.common.json_read import common_schema, example_schema
from .response_headers import add_headers
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error404,
                                                         Error422, Error500)
from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productCatalog",
    tags=["category"]
)


@router.get('/category',
            response_model=Union[ProductCategory, Error400, Error401, Error403, Error404, Error500],
            status_code=200,
            responses={
                200: example_schema["list_response_category_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                500: common_schema["response_500"],
                }
            )
def lists_or_finds_category_objects(
    response: Response,
    lifecycleStatus: Optional[str] = Query(
        "",
        description="Lifecycle Status of the Category",
        enum=["active", "obsolete"]),
    parentCategory_name: Optional[str] = Query(
        "",
        description="Name of the the Parent of this Product Category.",
        alias="parentCategory.name"
    ),
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
        date_tuple = (lastUpdate_gt, lastUpdate_lt)
        for date_data in date_tuple:
                if date_data is not None:
                    isvalid_format = validate_datetime_format(date_data)
                    if isvalid_format:
                        return isvalid_format
                    
        if offset is not None and offset < 0:
            status_msg_code = 400
            message = "'offset' cannot be negative"
            reason = "Invalid offset value"
            reference_error = None
            message_code = "invalidQuery"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if limit is not None and limit < 0:
            status_msg_code = 400
            message = "'limit' cannot be negative"
            reason = "Invalid limit value"
            reference_error = None
            message_code = "invalidQuery"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        if offset is None: offset = 0
        if limit is None: limit = 10

        current_directory = Path(__file__).parents[1]
        response_file = 'catalog_category_response.json'
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found {response_file}"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        extracted_data = []
        for _, category_info in json_data.items():
            json_parentCategory = category_info.get("name")
            json_lifecycleStatus = category_info.get("lifecycleStatus")
            json_lastUpdate = category_info.get("lastUpdate")
            json_buyerId = category_info.get("buyerId")
            json_sellerId = category_info.get("sellerId")
            
            if ((lifecycleStatus == "" or lifecycleStatus == json_lifecycleStatus) and
                (parentCategory_name == ""  or parentCategory_name == json_parentCategory) and
                (lastUpdate_lt is None  or (lastUpdate_lt and lastUpdate_lt >= json_lastUpdate)) and
                (lastUpdate_gt is None  or (lastUpdate_gt and lastUpdate_gt < json_lastUpdate)) and
                (buyerId == ""  or buyerId == json_buyerId) and
                (sellerId == ""  or sellerId == json_sellerId)
                ):
                extracted_info = {
                    "id": category_info.get("id"),
                    "href": category_info.get("href"),
                    "name": category_info.get("name"),
                    "description": category_info.get("description"),
                    "lastUpdate": category_info.get("lastUpdate"),
                    "lifecycleStatus": category_info.get("lifecycleStatus"),
                    "parentCategory": category_info.get("parentCategory"),
                    "subCategory": category_info.get("subCategory"),
                    "productOffering": category_info.get("productOffering"),
                }
                extracted_data.append(extracted_info)
        limited_responses = extracted_data[offset : offset + limit]    
        if not limited_responses or not extracted_data:
            status_msg_code = 404
            message = "No matching result found for the given criteria."
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        limited_responses_schema = [ProductCategory(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        validation = validate_list_category(json_data, parentCategory_name, lifecycleStatus)
        if validation is True:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8")
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.get('/category/{id}', response_model=Union[ProductCategory, Error400, Error401, Error403, Error422, Error500],
             status_code=status.HTTP_200_OK,responses={
                200: example_schema["list_response_category_200"],
                400: common_schema["response_400"],
                401: common_schema["response_401"],
                403: common_schema["response_403"],
                404: common_schema["response_404"],
                422: common_schema["response_422"],
                500: common_schema["response_500"],
                }
            )

async def retrieves_category_by_id(
    response: Response,
    id: str = Path(description = "Identifier of the category"),
    buyerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the requester represents more than one Buyer.",
    ),
    sellerId: Optional[str] = Query(
        "",
        description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the responding entity represents more than one Seller.",)
    ):
    """
    This operation retrieves a Category entity.
    """
    add_headers(response)
    try:
        current_directory = Path(__file__).parents[1]
        response_file = 'catalog_category_response.json'
        file_name = current_directory / 'responses'/response_file

        if not file_name.exists():
            status_msg_code = 404
            message = f"File not found {response_file}"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)
        except json.JSONDecodeError:
            status_msg_code = 404
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        
        all_values = json_data.values()
        found_id =False
        for category in all_values:
            if category["id"] == id:
                found_id =True
                json_result = category
                if buyerId != "":
                    if not check_buyer_id(json_result, buyerId): 
                        status_msg_code = 404
                        message = f"buyerId mismatch '{buyerId}'"
                        reason = "Requested buyerId not found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
                if sellerId != "":
                    if not check_seller_id(json_result, sellerId):
                        status_msg_code = 404
                        message = f"sellerId mismatch '{sellerId}'"
                        reason = "Requested sellerId not Found"
                        reference_error = None
                        message_code = "notFound"
                        property_path = None
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        if not found_id:   
            status_msg_code = 404
            message = f"Id not found '{id}'"
            reason = "'Id' not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

        validation = validate_category(json_data, id)
        if validation is True:
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=json_result,
            media_type="application/json;charset=utf-8")
        else:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
