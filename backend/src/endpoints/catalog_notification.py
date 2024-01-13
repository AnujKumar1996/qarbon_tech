from fastapi import APIRouter, Response, status
from src.common.json_read import common_schema
from src.schemas.sonata_schemas.product_catalog_notification_schema import ProductCategoryEvent,ProductOfferingEvent,ProductSpecificationEvent
from src.common.exceptions import raise_exception
from src.notification_operations.product_catagory_createEvent import category_create_event_notification
from src.notification_operations.product_catagory_status_create_event import category_status_create_event_notification
from src.notification_operations.catalog_product_offering_status_change_event import catalog_product_offering_status_change_event
from src.notification_operations.productoffering_create_event import productoffering_create_event_notification
from src.notification_operations.product_specification_create_event import productspecification_create_event_notification
from src.notification_operations.productoffering_attributevalue_change_event import catalog_productoffering_attributevalue_change_event
from src.notification_operations.product_specification_status_change_event import productspecification_status_change_event_notification
from src.notification_operations.productspecification_attribute_value_change_event import productspecification_attribute_value_change_event
from src.notification_operations.category_attribute_value_change_event import category_attributevalue_change_event

router = APIRouter(
    prefix="/v1/MEF/lsoSonata/productCatalogNotifications/productCatalog/listener",
    tags=["Product Catalog Notification Listeners"]
)
      
@router.post("/categoryCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_categorycreateevent(info:ProductCategoryEvent):
    """
    Client listener for receiving the notification CategoryCreateEvent
    """
    try:
       return category_create_event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
@router.post("/categoryStatusChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_categorystatuscreateevent(info:ProductCategoryEvent):
    """
    Client listener for receiving the notification categoryStatusChangeEvent
    """
    try:
       return category_status_create_event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/productOfferingCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_productofferingcreateevent(info:ProductOfferingEvent):
    """
    Client listener for receiving the notification ProductOfferingCreateEvent
    """
    try:
       return productoffering_create_event_notification(info)
   
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/productOfferingStatusChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
}) 
def client_listener_for_entity_productofferingstatuschangeevent(info:ProductOfferingEvent):
    """
    Client listener for receiving the notification ProductOfferingStatusChangeEvent
    """
    try:
       return catalog_product_offering_status_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/productSpecificationCreateEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})             
def client_listener_for_entity_productspecificationcreateEvent(info:ProductSpecificationEvent):
    """
    Client listener for receiving the notification ProductSpecificationCreateEvent
    """
    try:
       return productspecification_create_event_notification(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

@router.post("/productSpecificationAttributeValueChangeEvent", status_code=status.HTTP_204_NO_CONTENT,response_class = Response,
    responses = {
        204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        408: common_schema["response_408"],
        500: common_schema["response_500"]
        
    } )
def client_listener_for_entity_productspecificationattributevaluechangeevent(info:ProductSpecificationEvent):
    """
    Client listener for receiving the notification ProductSpecificationAttributeValueChangeEvent
    """
    try:
        return productspecification_attribute_value_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

   
@router.post("/productSpecificationStatusChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
})

def client_listener_for_entity_productspecificationcreateevent(info:ProductSpecificationEvent):
    """
    Client listener for receiving the notification ProductSpecificationCreateEvent
    """
    try:
       return productspecification_status_change_event_notification(info)
   
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    
@router.post("/categoryAttributeValueChangeEvent", status_code = status.HTTP_204_NO_CONTENT, response_class = Response,
             responses = {
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    } )
def client_listener_for_entity_categoryattributevaluechangeevent(info:ProductCategoryEvent ):
    '''
    Client listener for receiving the notification CategoryAttributeValueChangeEvent
    '''
    try:
        return category_attributevalue_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


@router.post("/productOfferingAttributeValueChangeEvent",status_code=status.HTTP_204_NO_CONTENT,response_class=Response,
    responses={
    204: {"description": "No Content (https://tools.ietf.org/html/rfc7231#section-6.3.5)"},
    400: common_schema["response_400"],
    401: common_schema["response_401"],
    403: common_schema["response_403"],
    408: common_schema["response_408"],
    500: common_schema["response_500"]
    
}) 
def client_listener_for_entity_productofferingattributevaluechangeEvent(info:ProductOfferingEvent):
    """
    Client listener for receiving the notification ProductOfferingAttributeValueChangeEvent
    """
    try:
       return catalog_productoffering_attributevalue_change_event(info)
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
