from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from src.schemas.sonata_schemas.common_schemas import Note, MEFBuyerSellerType


class ProductSpecificationLifecycleStatusType(str, Enum):
    """
    | Name                  | MEF 127 Name             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    | ----------------------| -------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | active                | ACTIVE                   | When a Product Specification has been defined and will be made available for ordering; however, it is not yet generally available.                                                                                                                                                                  |
    | endOfSale             | END_OF_SALE              | The endOfSale status means that Product Specification cannot be used for creation of a new Product Offerings.                                                                                                                                                                                       |
    | endOfSupport          | END_OF_SUPPORT           | When a Product Specification in the endOfSale status is no longer supported, the status transitions to endOfSupport. Any existing products can no longer be Changed, with the only Order action allowed is Disconnect.                                                                              |
    | obsolete              | OBSOLETE                 | After a Product Specification that is no longer available it transitions to obsolete and may be removed at the Seller’s discretion from the Product Catalog. This is a final state.                                                                                                                 |
    | onHold                | ON_HOLD                  | A Product Specification that has been orderable, but is currently not available for Buyers due to supply constraints, product recall or other issues preventing it to be offered.                                                                                                                   |
    | orderable             | ORDERABLE                | A Product Specification is in the orderable state when it is available for ordering by Buyers.                                                                                                                                                                                                      |
    | inTest                | PILOT_BETA               | When a Product Specification starts Pilot/Beta testing, it starts in the inTest state.                                                                                                                                                                                                              |
    | rejected              | REJECTED                 | When Pilot/Beta testing fails the Product Specification to the rejected state. This is a final state.                                                                                                                                                                                               |               
    |                       |                          |                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                           |
   
    """
    
    ACTIVE = "active"
    ENDOFSALE = "endOfSale"
    ENDOFSUPPORT = "endOfSupport"
    OBSOLETE = "obsolete"
    ONHOLD = "onHold"
    ORDERABLE = "orderable"
    INTEST = "inTest"
    REJECTED = "rejected"
    
   
class ProductSpecification_common(BaseModel) :

    id:str =Field(description="Unique identifier (within the Seller domain) for the Product Specification.")
    href: Optional[str] = Field(
        default="",
        description="Reference of the Product Specification"
    )
    name:str=Field(description="The commercial name of the Product Offering")
    lifecycleStatus:ProductSpecificationLifecycleStatusType 
    lastUpdate:datetime = Field(description="The date and time the Product Offering was created or most recently updated.")
    
class ProductSpecification_Find(ProductSpecification_common): 
    """
    Is a lightweight version of the Product Specification object used in Get List use case.
    """

class DataSizeUnit(str, Enum):
    BYTES = 'BYTES'
    KBYTES = 'KBYTES'
    MBYTES = 'MBYTES' 
    GBYTES = 'gbytes'
    TBYTES = 'GBYTES'
    PBYTES = 'PBYTES'
    EBYTES = 'EBYTES'
    ZBYTES = 'ZBYTES'
    YBYTES = 'YBYTES' 
    
class MEFByteSize(BaseModel):
    amount: float = Field(default=1, description="Numeric value in a given unit")
    units: Optional[DataSizeUnit] = Field(description="The unit of measure in the data size.")

class SchemaRefOrValue(BaseModel):
    '''
    Reference to the JSON schema location or the exact value of the JSON schema. Note: One of the properties must be provided i.e. schemaLocation or schema.
    '''
    rawSchema: Optional[str] = Field(default = "", description = "Raw JSON schema value.", alias = "schema")
    schemaLocation: Optional[str] = Field(default = "", description="Link to the schema describing the target product")

class AttachmentValue(BaseModel):
    '''
    Complements the Product Offering description with presentation, video, pictures, etc. This would only be expected to be used to provide additional information if there is a CPE re-quired, for instance a link to the website of the CPE vendor.
    '''
    attachmentId: Optional[str] = Field(default="", description="Locally unique identifier for items in the Attachment list.")
    author: str = Field(description="The name of the person or organization who added the Attachment.")
    content: Optional[str] = Field(default="", description="Actual contents of the attachment object, if embedded and encoded as base64.")
    creationDate: datetime = Field(description="The date the Attachment was added.")
    description: Optional[str] = Field(default="", description="Narrative text describing the content of the attachment.")
    mimeType: Optional[str] = Field(default="", description="Attachment mime type, such as extension file for video, picture, and document.")
    name: str = Field(description="The name of the attachment.")
    size: Optional[MEFByteSize] = Field( description="Size represented by value and Byte units")
    source: MEFBuyerSellerType = Field(description="Enumeration with buyer and seller values.")
    url: Optional[str] = Field(default="", description="URL where the attachment is located. Either URL or (content and mimeType) attributes must be provided during creation.")



class ProductSpecificationRelationship(BaseModel):
    '''
    Uni-directional relationship between the Products (the owner of the relation is the Product that defines it). Relation defines the type and the cardinalities.
    '''
    id: str = Field(description="Identifier of the targeted Product Specification")
    relationshipType: Optional[str] = Field(default="", description="Defines the type of the relation or the role of the relation owner in the context of this relation (e.g., hosts, aggregates)")
    minCardinality: Optional[int] = Field(default=0, minimum=0, description="Defines the type of the relation or the role of the relation owner in the context of this relation (e.g., hosts, aggregates)")
    maxCardinality: Optional[int] = Field(maximum=-1, default=-1, description="Maximal number of the related Products that must be satisfied. -1 stands for infinity.")

class ProductSpecification(BaseModel):
    '''
    Is a detailed description of a tangible or intangible object made available externally in the form of a ProductOffering to customers or other parties playing a party role.
    '''
    id: str = Field(description = "Unique identifier (within the Seller domain) for the Product Specification.")
    href: Optional[str] = Field(default = "", description="Reference of the Product Specification")
    name: str = Field(description = "Name of the Product Specification")
    lifecycleStatus: ProductSpecificationLifecycleStatusType
    lastUpdate: datetime = Field(description = "Date and time the Product Specification was created or most recently updated.")
    brand: Optional[str] = Field(default = "", description="Manufacturer or trademark of the Product Specification if the Seller requires a CPE on the Buyer's premise.")
    description: str = Field(description = "Description of the Product Offering")
    productNumber: Optional[str] = Field(default = "", description="Identifier assigned to the model or version of the CPE used in conjunction with the Brand.")
    attachment: Optional[List[AttachmentValue]]
    note: Optional[List[Note]] = Field(description = "Extra information about a given entity. Only useful in processes involving human interaction. Not applicable for the automated process.")
    sourceSchema: SchemaRefOrValue 
    productSpecificationRelationship: List[ProductSpecificationRelationship] = Field(description = "List of relations between defined Product Specifications.")
    
