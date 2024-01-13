from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from .common_schemas import  Note, RelatedContactInformation

class ProductOfferingLifecycleStatusType(str, Enum):
    """
    | Name               | MEF 127 Name | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
    | ------------------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | active             | ACTIVE        | When a Product Offering or Product Specification has been defined and will be made available for ordering; however, it is not yet generally available.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    | endOfSale          | END_OF_SALE   | The Product Offering or Product Specification cannot be Installed by any new or existing Buyers, but Buyers may still have Products in use and may Change or Disconnect it, and receive support.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
    | endOfSupport       | END_OF_SUPPORT| When a Product Offering or Product Specification in the endOfSale state is no longer supported, the status transitions to endOfSupport. Any existing products can no longer be modified, with the only Order action allowed is delete.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
    | obsolete           | OBSOLETE      | After a Product Offering or Product Specification that is no longer available it transitions to obsolete and may be removed at the Seller's discretion from the Product Catalog. This is a final state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
    | onHold             | ON_HOLD       | A Product Offering or Product Specification that has been orderable, but is currently not available for Buyers due to supply constraints, product recall or other issues preventing it to be offered.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
    | orderable          | ORDERABLE     | A new Product Offering or Product Specification is in the orderable state when it is available for ordering by Buyers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
    | inTest             | PILOT_BETA     | When a Product Offering or Product Specification starts Pilot/Beta testing, it starts in the pilotBeta state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
    | rejected           | REJECTED      | When PILOT_BETA testing fails the Product Offering or Product Specification transitions to the rejected state. This is a final state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    """
    ACTIVE = "active"
    ENDOFSALE = "endOfSale"
    ENDOFSUPPORT = "endOfSupport"
    OBSOLETE = "obsolete"
    ONHOLD = "onHold"
    ORDERABLE = "orderable"
    INTEST = "inTest"
    REJECTED = "rejected"

class Region(BaseModel):
    
    locality: Optional[str] = Field(
        default="",
        description="An area of defined or undefined present boundaries within a local authority or other legislatively defined area, usually rural or semi-rural in nature."
    )
    stateOrProvince: Optional[str] = Field(
        default="",
        description="The State or Province that the address is in."
    )
    country: str = Field(
        description="The Country the region is located."
    )

class CategoryRef(BaseModel):
    """
    The list of Product Category References in which this Product Offering is grouped together with other Product Offerings available to the Buyer.
    """
    id: str = Field(description="Unique (within the Seller domain) identifier for the Category")
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to access the Category"
    )


class ProductOfferingLifecycleStatusTransition(BaseModel):
    """
    The planned Product Offering Status transition, including the date it is expected to occur.
    """
    transitionDate: Optional[datetime]= Field(
        description="The Date and Time that the Next Product Offering Status transition is planned to occur."
    )
    transitionLifecycleStatus:Optional[ProductOfferingLifecycleStatusType] = Field(default="",
        description="The status of the Product Offering on the planned Transition Date."
    )
class DataSizeUnit(str,Enum):
    """
    The unit of measure in the data size
    """
    BYTES="bytes"
    KBYTES="kbytes"
    MBYTES="mbytes"
    GBYTES="gbytes"
    TBYTES="tbytes"
    PBYTES="pbytes"
    EBYTES="ebytes"
    ZBYTES="zbytes"
    YBYTES="ybytes"
    
class MEFByteSize(BaseModel):
    """
    A size represented by value and Byte units
    """
    amount: float = Field(
        default=1,
        description="Numeric value in a given unit"
    )
    units: DataSizeUnit 

class TimeUnit(str,Enum):
    """
    Represents a unit of time. Reference: MEF 57.2 (Sn 9.22
    """
    CALENDARMONTHS="calendarMonths"
    CALENDARDAYS="calendarDays"
    CALENDARHOURS="calendarHours"
    CALENDARMINUTES="calendarMinutes"
    BUSINESSDAYS="businessDays"
    BUSINESSHOURS="businessHours"
    BUSINESSMINUTES="businessMinutes"

class Duration(BaseModel):
    """
    A Duration in a given unit of time e.g. 3 hours, or 5 days.
    """
    amount: int = Field(
        description="Duration (number of seconds, minutes, hours, etc.)"
    )
    units: TimeUnit 

class MEFBuyerSellerType(str,Enum):
    """
    An enumeration with buyer and seller values.
    """
    BUYER="buyer"
    SELLER="seller"

class AttachmentValue(BaseModel):
    """
    Complements the description of an element (for instance a product) through video, pictures...
    """

    attachmentId: Optional[str] = Field(default="",
        description="Locally unique identifier to distinguish items from the Attachment list."
    )
    author: str = Field(
        description="The name of the person or organization who added the Attachment."
    )
    content: Optional[str]  = Field(default="",
        description="The actual contents of the attachment object, if embedded, encoded as base64."
    )
    creationDate: datetime = Field(
        description="The date the Attachment was added."
    )
    description: Optional[str]  = Field(default="",
        description="A narrative text describing the content of the attachment."
    )
    mimeType: Optional[str]  = Field(default="",
        description="Attachment mime type such as extension file for video, picture and document."
    )
    name: str = Field(
        description="The name of the attachment."
    )
    size: Optional[MEFByteSize] = Field(default=None,
        description="The size of the attachment."
    )
    source: MEFBuyerSellerType = Field(default=None,
        description="Indicates if the attachment was added by the Buyer or the Seller."
    )
    url: Optional[str]  = Field(default="",
        description="URL where the attachment is located."
    )

class MEFEndOfTermAction(str,Enum):
    """
    The action the Seller will take once the term expires. Roll indicates that the Product's contract will continue on a rolling basis for the duration of the Roll Interval at the end of the Term.
    Auto-disconnect indicates that the Product will be disconnected at the end of the Term. Auto-renew indicates that the Product's contract will be automatically renewed for the Term Duration at the end of the Term.
    """
    ROLL="roll"
    AUTODISCONNECT="autoDisconnect"
    AUTORENEW="autoRenew"

class MEFItemTerm(BaseModel):
    """
    The term of the Item
    """
    description: Optional[str] = Field(default="",
        description="Description of the term."
    )
    duration: Duration = Field(default=None,
        description="Duration of the term."
    )
    endOfTermAction: MEFEndOfTermAction = Field(default=None,
        description="The action that needs to be taken by the Seller once the term expires."
    )
    name: str = Field(
        description="Name of the term."
    )
    rollInterval: Optional[Duration] = Field(default=None,
        description="The recurring period that the Buyer is willing to pay for the Product after the original term has expired."
    )


class ProductSpecificationRef(BaseModel):
    """"
     Product Specification reference.
    """
    id: str = Field(
        description="Unique (within the Seller domain) identifier for the Product Specification."
    )
    href: Optional[str] = Field(default="",
        description="Hyperlink to access the Product Specification."
    )
class SchemaRefOrValue(BaseModel):
    """
    Reference to the JSON schema location or the exact value of the JSON schema. Note: One of the properties must be provided i.e. schemaLocation or schema.
    """
    rawSchema:Optional[str]=Field(default="",description="Raw JSON schema value.", alias = "schema")
  
    schemaLocation:Optional[str]=Field(default="",description="This field provides a link to the schema describing the target product")

class MEFProductAction(str,Enum):
    """
    Action that could be applied to the Product (or future product) during the execution of the Business Function. Value 'All' is the wildcard - stands for any action
    """
    ADD="add"
    MODIFY="modify"
    ALL="all"

class MEFBusinessFunction(str,Enum):
    """
    Business Function that could be executed for the given Product accordingly to LSO Cantata/Sonata IRPs. Value 'All' is the wildcard - stands for any action.
    """

    PRODUCTOFFERINGQUALIFICATION="productOfferingQualification"
    QUOTE="quote"
    PRODUCTORDER="productOrder"
    PRODUCTINVENTORY="productInventory"
    ALL="all"

class Context(BaseModel):
    """
    Context that is defined as a two-dimensional vector of Business Function and Product Action.
    """
    productAction:Optional[MEFProductAction]=Field(default="")
    businessFunction:Optional[MEFBusinessFunction]=Field(default="")


class ProductOfferingContextualInfo(BaseModel):
    """
    Constrained Product Schema that should be used by the Buyer in the defined Context, where Context is built as pair - a Business Function (e.g. Quote) and Product Action (e.g. install)./
    Those product schemas are created by applying the constraints to Product Schemas defined in the Product Specification./
    Contextual info MUST be provided for every possible combination of Product Actions and Business Functions (if there are no differences per function of per action then use wildcard - 'all' - and reuse the value of Product Offering Specification attribute).
    """
    contextSchema: SchemaRefOrValue = Field(default=None,
        description="Product Schema that is defined for the given Context."
    )
    context: Context = Field(default=None,
        description="Context that is defined as a two-dimensional vector of Business Function and Product Action."
    )


class ProductOffering(BaseModel):
    """
    Represents entities that are orderable from the provider of the catalog, this resource included all available information of Product Offering
    """
    id :str = Field(description="Unique identifier (within the Seller domain) for the Product Offering. Note - The Seller must create a new Product Offering Identifier for every new version of a Product Offering. The Seller may choose to incorporate the version information as part of the Offering Identifier.")
   
    href:Optional[str] = Field(default="", description="Hyperlink reference to the Product Offering")
  
    name:str = Field( description="The commercial name of the Product Offering")
   
    description:Optional[str] = Field(default="", description="Description of the Product Offering")
   
    lastUpdate:datetime = Field(description="The date and time the Product Offering was created or most recently updated.")
   
    lifecycleStatus:ProductOfferingLifecycleStatusType 
   
    agreement:str=Field(description="The name of the Seller's offer arrangement (such as a framework agreement). This may be a standard offer agreement or a customer specific agreement (e.g., for a customer specific Product Catalog or customer specific Product Offering). The name is unique within the Seller domain.")
   
    channel:List[str] = Field(description="The names of the sales channel through which the Product Offering is made available to the Buyer to order. The set of channel names should be specified in the Agreement or provided during the onboarding process. For example: reseller, distribution, directSales. Note: If channel is an empty list, it implies that the Product Offering is available in all Seller supported channels")
   
    marketSegment:List[str] = Field(default=None,description="The names of the market segments targeted for the Product Offering. The set of market segment names should be specified in the Agreement or provided during the onboarding process. For example: wholesale, federal, financial. Note: If marketSegment is an empty list, it implies that the Product Offering is available in all Seller supported market segments")
   
    region:List[Region] = Field(default=None,description="Areas where the products are offered by the Seller to potential Buyers. Note: If region is an empty list, it implies that the Product Offering is available in all Seller supported Regions.")
   
    category: List[CategoryRef] = Field(default=None,
        description="The list of Product Category References in which this Product Offering is grouped."
    )
   
    statusTransitions:Optional[List[ProductOfferingLifecycleStatusTransition]]=  Field(default=None)
   
    productOfferingStatusReason:Optional[str] = Field(default="",description="Provides complementary information on the reason why the Product Offering Lifecycle Status is set to a particular value.")
   
    attachment:Optional[List[AttachmentValue]] = Field(default=None,description="Complements the Product Offering description with presentation, video, pictures, etc.")
   
    relatedContactInformation:Optional[List[RelatedContactInformation]] = Field(default=None)
   
    productOfferingTerm:Optional[List[MEFItemTerm]] = Field(default=None,description="Commitment durations under which a Product Offering is available to Buyers. For instance, a Product Offering can be made available with multiple commitment periods of 1, 2 or 3 year terms.")
  
    note:Optional[List[Note]]=Field(default=None,description="A set of comments for additional information.")
  
    productSpecification:ProductSpecificationRef 
  
    productOfferingContextualInfo:Optional[List[ProductOfferingContextualInfo]] = Field(default=None,description="Defines additional constraints on the Product Offering Specification for use with the payload for a Product Offering for each Business Function and Product Action.")
  
    productOfferingSpecification:SchemaRefOrValue 
    
class ProductOffering_Find(BaseModel):
    id: str = Field(
        description="Unique identifier (within the Seller domain) for the Product Offering. Note - The Seller must create a new Product Offering Identifier for every new version of a Product Offering. The Seller may choose to incorporate the version information as part of the Offering Identifier."
    )
    href: Optional[str] = Field(
        default="",
        description="Hyperlink reference to the Product Offering."
    )
    name: str = Field(
        description="The commercial name of the Product Offering."
    )
    description: Optional[str] = Field(
        default="",
        description="Description of the Product Offering."
    )
    lastUpdate: str = Field(
        description="The date and time the Product Offering was created or most recently updated."
    )
    lifecycleStatus: ProductOfferingLifecycleStatusType
    agreement: str = Field(
        description="The name of the Seller's offer arrangement (such as a framework agreement). This may be a standard offer agreement or a customer specific agreement (e.g., for a customer specific Product Catalog or customer specific Product Offering). The name is unique within the Seller domain."
    )
    channel: List[str] = Field(
        description="The names of the sales channel through which the Product Offering is made available to the Buyer to order. The set of channel names should be specified in the Agreement or provided during the onboarding process. For example: reseller, distribution, directSales. Note: If channel is an empty list, it implies that the Product Offering is available in all Seller supported channels."
    )
    marketSegment: List[str] = Field(
        description="The names of the market segments targeted for the Product Offering. The set of market segment names should be specified in the Agreement or provided during the onboarding process. For example: wholesale, federal, financial. Note: If marketSegment is an empty list, it implies that the Product Offering is available in all Seller supported market segments"
    )
    region: List[Region] = Field(
        description="Areas where the products are offered by the Seller to potential Buyers. Note: If region is an empty list, it implies that the Product Offering is available in all Seller supported Regions."
    )
    category: List[CategoryRef] = Field(
        description="The list of Product Category References in which this Product Offering is grouped together with other Product Offerings available to the Buyer."
    )
