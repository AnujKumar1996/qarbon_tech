from pydantic import Field,BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from .common_schemas import Event

class ProductCategoryEventType(str,Enum):
    """
    Type of the Product Category event.

    | API name                           | MEF 127 name                 | Description                                                                      |
    |------------------------------------|------------------------------|----------------------------------------------------------------------------------|
    | `categoryCreateEvent`              | PRODUCT_CATEGORY_CREATE      | The Seller has published new Product Category to the Buyers.                     |
    | `categoryAttributeValueChangeEvent`| PRODUCT_CATEGORY_UPDATE      | The Seller settable attributes for a Product Category were updated by the Seller.|
    | `categoryStateChangeEvent`         | PRODUCT_CATEGORY_STATE_CHANG | A Product Category status was changed by the Seller.                             |
    """
    PRODUCT_CATEGORY_CREATE       = 'categoryCreateEvent'
    PRODUCT_CATEGORY_UPDATE       = 'categoryAttributeValueChangeEvent'
    PRODUCT_CATEGORY_STATE_CHANGE = 'categoryStateChangeEvent'

class ProductCategoryEventPayload(BaseModel):
    '''
    The identifier of the Product Category being subject of this event.
    event.
    '''
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when requester entity represents more than one Seller.")
    id : str = Field(description='ID of the Product Category attributed by the Seller')        
    href : Optional[str] = Field(default="", description='Hyperlink to access the Product Category')
    buyerId : Optional[str] = Field (default="", description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")

class ProductCategoryEvent(Event):
    '''
    Event class is used to describe information structure used for notification
    '''
    eventId : str = Field(description="Id of the event")
    eventTime : datetime = Field(description="Datetime when the event occurred")
    eventType : ProductCategoryEventType 
    event : ProductCategoryEventPayload
    
      
class ProductOfferingEventType(str,Enum):
    """
    Type of the Product Offering event.

    | API name                                  | MEF 127 name                  | Description                                                                      |
    |-------------------------------------------|-------------------------------|----------------------------------------------------------------------------------|
    | `productOfferingCreateEvent`              | PRODUCT_OFFERING_CREATE       | The Seller has published new Product Offering to the Buyers.                     |
    | `productOfferingAttributeValueChangeEvent`| PRODUCT_OFFERING_UPDATE       | The Seller settable attributes for a Product Offering were updated by the Seller.|
    | `productOfferingStateChangeEvent`         | PRODUCT_OFFERING_STATE_CHANGE | A Product Offering status was changed by the Seller.                             |
    """
    PRODUCT_OFFERING_CREATE       = 'productOfferingCreateEvent'
    PRODUCT_OFFERING_UPDATE       = 'productOfferingAttributeValueChangeEvent'
    PRODUCT_OFFERING_STATE_CHANGE = 'productOfferingStateChangeEvent'

class ProductOfferingEventPayload(BaseModel):
    '''
    The identifier of the Product Offering being subject of this event.
    '''
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when requester entity represents more than one Seller.")
    id : str = Field(description='ID of the Product Offering attributed by the Seller')        
    href : Optional[str] = Field(default="", description='Hyperlink to access the Product Offering')
    buyerId : Optional[str] = Field (default="", description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")

class ProductOfferingEvent(Event):
    '''
    Event class is used to describe information structure used for notification.
    '''
    eventType : ProductOfferingEventType 
    event : ProductOfferingEventPayload
 
    
class ProductSpecificationEventType(str,Enum):
    """
    Type of the Product Specification event.

    | API name                                       | MEF 127 name                       | Description                                                                      |
    |------------------------------------------------|------------------------------------|----------------------------------------------------------------------------------|
    | `productSpecificationCreateEvent`              | PRODUCT_SPECIFICATION_CREATE       | The Seller has published new Product Specification to the Buyers.                     |
    | `productSpecificationAttributeValueChangeEvent`| PRODUCT_SPECIFICATION_UPDATE       | The Seller settable attributes for a Product Specification were updated by the Seller.|
    | `productSpecificationStateChangeEvent`         | PRODUCT_SPECIFICATION_STATE_CHANGE | A Product Specification status was changed by the Seller.                             |
    """
    PRODUCT_SPECIFICATION_CREATE       = 'productSpecificationCreateEvent'
    PRODUCT_SPECIFICATION_UPDATE       = 'productSpecificationAttributeValueChangeEvent'
    PRODUCT_SPECIFICATION_STATE_CHANGE = 'productSpecificationStateChangeEvent'

class ProductSpecificationEventPayload(BaseModel):
    '''
    The identifier of the Product Specification being subject of this event.
    '''
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when requester entity represents more than one Seller.")
    id : str = Field(description='ID of the Product Specification attributed by the Seller')        
    href : Optional[str] = Field(default="", description='Hyperlink to access the Product Specification')
    buyerId : Optional[str] = Field (default="", description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")

class ProductSpecificationEvent(Event):
    '''
    Event class is used to describe information structure used for notification.
    '''
    eventType : ProductSpecificationEventType 
    event : ProductSpecificationEventPayload