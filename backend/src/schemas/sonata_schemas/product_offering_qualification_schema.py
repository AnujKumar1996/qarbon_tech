from pydantic import Field,BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from typing import List, Optional
from src.schemas.sonata_schemas.common_schemas import  RelatedContactInformation, MEFProductConfiguration
from pydantic import BaseModel, Field, HttpUrl

class PoqEventType(str,Enum):
    """
    Indicates the type of product offering qualification event.
    """
    POQCREATEEVENT = "poqCreateEvent"
    POQSTATECHANGEEVENT = "poqStateChangeEvent"
    POQITEMSTATECHANGEEVENT = "poqItemStateChangeEvent"

class PoqEvent(BaseModel):
    '''
    A reference to the POQ that is the source of the notification.
    '''
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the requester entity represents more than one Seller. Reference: MEF 79 (Sn 8.8)")
    poqItemId : Optional[str] = Field(default="", description="ID of the Poq Item (within the Poq) which state change triggered the event")
    id : str = Field(description = "The POQ unique identifier.", min_length=1)        
    href : Optional[str] = Field(default = "", description="Link to the POQ")
    buyerId : Optional[str] = Field (default = "", description="The unique identifier of the organization that is acting as the Buyer. MUST be specified in the request only when the responding represents more than one Buyer. Reference: MEF 79 (Sn 8.8)")

class Event(BaseModel):
    '''
    Event class is used to describe information structure used for notification. Reference: MEF 79 (Sn 8.5)
    '''
    eventId: str = Field(description = "Id of the event", min_length=1)
    eventTime: datetime = Field(description = "Date-time when the event occurred")
    eventType : PoqEventType 
    event : PoqEvent

class MEFPOQTaskStateType(str, Enum):
    """
    These values represent the valid states through which the product
    offering qualification can transition.
    
    | MEFPOQTaskStateType       | MEF 79                            | Description                                                                                                                         |
    | --------------------------| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------|
    | `acknowledged`            | N/A                               | A request has been received by the Seller, has passed basic validation and the id was assigned.                                     |
    | `done.ready`              | READY                             | Reached when all items are in `done` state                                                                                          |
    | `done.unableToProvide`    | UNABLE_TO_PROVIDE                 | This state is set when the Seller is unable to provide a Product Offering Qualification in the timeframe required by the Buyer.     |
    | `terminatedWithError`     | INSUFFICIENT_INFORMATION_PROVIDED | This state is achieved when a well-formed POQ request has been received, but there is insufficient information to complete the POQ. |
    | `inProgress`              | IN_PROGRESS                       | There is at least one POQ Item in `inProgress` state                                                                                |
    """
    ACKNOWLEDGED = 'acknowledged'
    READY = 'done.ready'
    UNABLE_TO_PROVIDE = 'done.unableToProvide'
    TERMINATED_WITH_ERROR = 'terminatedWithError'
    IN_PROGRESS = 'inProgress'


class ProductOfferingQualification_Find(BaseModel):
    """
    This class represents a single list item for the response of
    `listProductOfferingQualification` operation.
    Reference: MEF 79 (Sn 8.6)
    """
    id: str = Field(
        description="The POQ Request's unique identifier.",
        min_length=1
    )
    externalId: Optional[str] = Field(
        default="",
        description="ID given by the consumer and only understandable by him (to facilitate his searches afterwards)."
    )
    state: MEFPOQTaskStateType
    projectId: Optional[str] = Field(
        default="",
        description="The project ID specified by the Buyer in the POQ Request, if any."
    )
    requestedPOQCompletionDate: Optional[str] = Field(
        default=None,
        description="The latest date the POQ completion is expected by the Buyer, if specified by the Buyer.",
        format="date-time",
    )


class RelatedPlaceRefOrValue(BaseModel):
    """
    Place defines the places where the product order must be done.
    """
    schemaLocation: Optional[str] = Field(
        default=None,
        alias="@schemaLocation",
        description="A URL to a JSON-Schema file that defines additional attributes and relationships. May be used to define additional related place types. Usage of this attribute must be agreed between Buyer and Seller.",
        pattern=r'^https?://\S+$'
        )
    type: str = Field(
        alias="@type",
        example="FieldedAddress",
        description="This field is used as discriminator. The value is the name of one of the types that inherit from it using 'allOf', i.e. one of FieldedAddress, FormattedAddress, GeographicAddressLabel, MEFGeographicPoint, GeographicAddressRef, GeographicSiteRef. Moreover, it might discriminate for an additional related place as defined in '@schemaLocation'.", 
        min_length=1
        )
    role: str = Field(
        description="Role of this place. The values that can be specified here are described by Product Specification.",  
        min_length=1
        )    
    
class ProductSpecificationRef(BaseModel):
    """"
    A reference to a structured set of well-defined technical attributes and/or behaviors that are used to construct a Product Offering for sale to a market.
    """
    id: str = Field(
        description="Unique identifier for the Product Specification.", 
        min_length=1
    )
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to a Product Specification in Sellers catalog. In case Seller is not providing a catalog API this field is not used. The catalog is provided by the Seller to the Buyer during onboarding. Hyperlink MAY be used by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request."
    )  
    
class ProductOfferingRef(BaseModel):
    """
    A reference to a Product Offering offered by the Seller to the Buyer. 
    A Product Offering contains the commercial and technical details of a Product sold by a particular Seller. 
    A Product Offering defines all of the commercial terms and, through association with a particular Product Specification, defines all the technical attributes and behaviors of the Product. 
    A Product Offering may constrain the allowable set of configurable technical attributes and/or behaviors specified in the associated Product Specification. Defined in MEF 79 Section 8.4.1.1
    """
    id: str = Field(
        description="id of a Product Offering. It is assigned by the Seller. The Buyer and the Seller exchange information about offerings' ids during the onboarding process.", 
        min_length=1
        )
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to a Product Offering in Sellers catalog. In case Seller is not providing a catalog API this field is not used. The catalog is provided by the Seller to the Buyer during onboarding. Hyperlink MAY be used by the Seller in responses Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request."
        ) 
class ProductRelationshipWithGrouping(BaseModel):
    """
    A relationship to existing Product. The requirements for usage for given Product are described in the Product Specification. 
    The "WithGrouping" flavour of the Product Relationship allows for providing a list of related product identifiers within a single Product Relationship. 
    This can be later used while processing the request as defined in the Product Specification. The groupingKey attribute is used to achieve this behavior in the API by marking the list of ProductRelationshipWithGroupings within a product with a common key.
    """
    relationshipType: str = Field(
        description="Specifies the type (nature) of the relationship to the related Product. The nature of required relationships varies for Products of different types. For example, a UNI or ENNI Product may not have any relationships, but an Access E-Line may have two mandatory relationships (related to the UNI on one end and the ENNI on the other). More complex Products such as multipoint IP or Firewall Products may have more complex relationships. As a result, the allowed and mandatory relationshipType values are defined in the Product Specification.", 
        min_length=1
    )   
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to the product in Seller's inventory that is referenced Hyperlink MAY be set by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request."
    ) 
    id: str = Field(
        description="unique identifier of a Product that is referenced", 
        min_length=1
    ) 
    groupingKey: Optional[str] = Field(
        default="",
        description="MEF 79.0.1. Introduces a list of related ids for the ProductRelationship. For sake of TMF compliance, a groupingKey is introduced to retain id as a simple attribute. Ids from relationships having the same groupingKey and relationshipType MUST be treated as a list of identifiers. Reference: MEF 79.0.1 (Sn 7)"
    ) 
   
class MEFProductRefOrValue(BaseModel):
    """
    Used by the Buyer to point to existing and/or describe the desired shape of the product. 
    In case of add action - only productConfiguration MUST be specified. For modify action - both id and productConfiguration MUST be provided to point which product instance to update and to what state. 
    In delete only the id must be provided.
    """
    productSpecification: Optional[ProductSpecificationRef] = Field(default=None)
    productOffering: Optional[ProductOfferingRef] = Field(default=None)
    productConfiguration :Optional[MEFProductConfiguration] = Field(default=None)
    productRelationship : Optional[List[ProductRelationshipWithGrouping]] = Field(default=None,description= "A list of references to existing products that are related to the Product that would be delivered to fulfill the POQ Item.")
    href:Optional[str] = Field(
        default="",
        description="Hyperlink to the referenced Product. Hyperlink MAY be used by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request."
        )
    id: Optional[str] = Field(
        default="",
        description="The unique identifier of an in-service Product that is the qualification's subject. This field MUST be populated if an item action is either modify or delete. This field MUST NOT be populated if an item action is add."
    )
    place: Optional [List[RelatedPlaceRefOrValue]] = Field(
        default=None,
        description="A list of locations that are related to the Product. For example an installation location"
    )
    
class QualificationItemRelationship(BaseModel):
    relationshipType:str = Field(description="One of the relationship types defined in the Product Specification.", 
        min_length=1)    
    id : str = Field(description="An identifier of the targeted POQ item within the same POQ request",
    min_length=1)
   
class ProductActionType(str, Enum):
    """
    Action to be performed on the Product Item. The action types are described in MEF 79 (Sn 8.4.1.1).
    The following mapping has been used between ProductActionType and MEF 79:

    | ProductActionType | MEF 57.2   |
    | ----------------- | ---------- |
    | add               | INSTALL    |
    | modify            | CHANGE     |
    | delete            | DISCONNECT |
    """
    ADD     = 'add'
    MODIFY  = 'modify'
    DELETE  = 'delete' 
       
class ProductOfferingQualificationItem_Create(BaseModel):
    """
    This structure serves as a request for a product offering qualification item.
    A product qualification item is an individual article included in a POQ that describes a Product of a particular type (Product Offering) being delivered to the geographic address or a service site specified by the Buyer.
    The objective is to determine if it is feasible for the Seller to deliver this item as described and for the Seller to inform the Buyer of the estimated time interval to complete this delivery. 
    The modelling pattern introduces the Common supertype to aggregate attributes that are common to both ProductOfferingQualificationItem and ProductOfferingQualificationItem_Create. 
    It happens that it is the Create type has a subset of attributes of the response type and does not introduce any new, thus the Create type has an empty definition. Reference: MEF 79 (Sn 8.4.1.1)
    """    
    product : MEFProductRefOrValue
    qualificationItemRelationship : Optional[List[QualificationItemRelationship]] = Field(default=None,description="A list of references to related POQ items in this POQ")
    relatedContactInformation : Optional[List[RelatedContactInformation]] = Field(default=None, description="Contact information of an individual or organization playing a role for this POQ Item (e.g. for MEF 79: POQ Item Location Contact, role=locationContact)")
    action : ProductActionType
    id : str = Field(description="Id of this POQ item which is unique within the POQ. Assigned by the Buyer.", 
        min_length=1)

class ProductOfferingQualification_Create(BaseModel):
    """
    Represents a request formulated by the Buyer that is composed of product offering qualification items. Reference: MEF 79 (Sn 8.4)
    """
    externalId:Optional[str] = Field(
        default="",
        description="ID given by the consumer and only understandable by him (to facilitate his searches afterwards)"
        ) 
    instantSyncQualification: bool = Field(
        default=False,
        description="If this flag is set to Yes, Buyer requests to have an instant qualification to be provided in operation POST response"
        )
    relatedContactInformation: List[RelatedContactInformation] = Field(description="Party playing a role for this qualification. MEF 79 mandates providing 'Buyer Contact Information' in the request ('role=buyerContactInformation') and 'Seller Contact Information' in the response ('role=sellerContactInformation')")
    
    provideAlternative: Optional[bool] = Field(
        default=False,
        description="Allows the Buyer to indicate if he is willing to get an alternate proposal if requested product not available."
        ) 
    projectId: Optional[str] = Field(
        default="",
        description="This value MAY be assigned by the Buyer to identify a project the serviceability request is associated with."
        )
    requestedPOQCompletionDate: Optional[datetime] = Field(
        default=None,
        description="The latest date a the POQ completion is expected. This attribute is required when instantSyncQualification=false"
        )
    productOfferingQualificationItem:List[ProductOfferingQualificationItem_Create] = Field(description="A non-empty list of POQ items")
   
class MEFServiceabilityColor(str, Enum):
    '''
    A color that indicates confidence to service the request. When the item
    state is `done.ready` the Seller **MUST** provide a value. It MUST
    NOT be populated for other states.
    Mapping between `ServiceabilityColor` and POQ Confidence Level:
    | ServiceabilityColor      | MEF 79       | MEF 79 semantics                                                              |
    |------------------------- | ------------ | ----------------------------------------------------------------------------- |
    | green                    | GREEN        |  The Seller has high confidence that this Product can be delivered            |
    | yellow                   | YELLOW       |  The Seller believes they can deliver the Product but is not highly confident |
    | red                      | RED          |  The Seller cannot deliver the Product as specified                           |
    Reference: MEF 79 (Sn 8.4.3.1)
    '''
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    
class TimeUnit(str, Enum):
    """Represents a unit of time. Reference: MEF 79 (Sn 8.4.3.1/8.4.3.2)"""
    CALENDARMONTHS  = 'calendarMonths'
    CALENDARDAYS  = 'calendarDays'
    CALENDARHOURS  = 'calendarHours'
    CALENDARMINUTES = 'calendarMinutes'
    BUSINESSDAYS = 'businessDays'
    BUSINESSHOURS  = 'businessHours'
    BUSINESSMINUTES = 'businessMinutes'
    
class Duration(BaseModel):
    """A Duration in a given unit of time, e.g., 3 hours, or 5 days."""
    amount: int = Field(description="Duration (number of seconds, minutes, hours, etc.)")
    units: TimeUnit
    
class MEFAlternateProduct(BaseModel):
    """An alternative Product Offering proposed by the Seller."""
    productSpecification: Optional[ProductSpecificationRef] = Field(default=None)
    productOffering: ProductOfferingRef
    productConfiguration: MEFProductConfiguration
    
class AlternateProductOfferingProposal(BaseModel):
    """
    If in the request the Buyer has requested to have alternate product
    proposals, then this class represents a single proposal. All properties
    are assigned by the Seller.
    Reference: MEF 79 (Sn 8.4.3.2)
    """
    installationInterval: Duration
    id: str = Field(description="Identifier of the Product Offering Qualification alternate proposal. Assigned by the Seller.", 
                    min_length=1)
    alternateProduct: MEFAlternateProduct
    
class Error422Code(str, Enum):
    """
    One of the following error codes:
      - missingProperty: The property the Seller has expected is not present in the payload
      - invalidValue: The property has an incorrect value
      - invalidFormat: The property value does not comply with the expected value format
      - referenceNotFound: The object referenced by the property cannot be identified in the Seller system
      - unexpectedProperty: Additional property, not expected by the Seller has been provided
      - tooManyRecords: the number of records to be provided in the response exceeds the Seller's threshold.
      - otherIssue: Other problem was identified (detailed information provided in a reason)
    """
    MISSINGPROPERTY  = "missingProperty"
    INVALIDVALUE  = "invalidValue"
    INVALIDFORMAT  = "invalidFormat"
    REFERENCENOTFOUND  = "referenceNotFound"
    UNEXPECTEDPROPERTY  = "unexpectedProperty"
    TOOMANYRECORDS  = "tooManyRecords"
    OTHERISSUE  = "otherIssue"
    
class TerminationError(BaseModel):
    """
This indicates an error that caused an Item to be terminated. The code and propertyPath should be used like in Error422."""
    code: Optional[Error422Code] = Field(default="", description="This indicates an error that caused an Item to be terminated. The code and propertyPath should be used like in Error422.")
    propertyPath: Optional[str] = Field(default="", description="A pointer to a particular property of the payload that caused the validation issue. It is highly recommended that this property should be used. Defined using JavaScript Object Notation (JSON) Pointer (https://tools.ietf.org/html/rfc6901).")
    value: Optional[str] = Field(default="", description="Text to describe the reason of the termination.")
    
class MEFPOQItemTaskStateType(str, Enum):
    """
    POQ item states - The specific states are managed by the Seller based on
    its processing and/or based on the Buyer's action. The following mapping
    has been used between `MEFPOQItemTaskStateType` and MEF 79 (Sn 9.2):
    | MEFPOQItemTaskStateType | MEF79                             | Description                                                                                                                  |
    | ----------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
    | acknowledged            | N/A                               | A request has been received by the Seller and has passed basic validation.                                                   |
    | done.ready              | READY                             | POQ Item response is complete. This state does not imply that Seller is able to deliver the requested item.                 |
    | done.abandoned          | ABANDONED                         | Applied to a POQ Item in case the final state is not reached, and any other POQ Item moved to the final state other than done |
    | terminatedWithError     | INSUFFICIENT_INFORMATION_PROVIDED | The information provided by the Buyer is insufficient for the Seller to provide a POQ Item response.                         |
    | inProgress              | IN_PROGRESS                       | The Seller is working on a POQ item response, and the answer is not ready yet.                                               |
    """
    ACKNOWLEDGED  = "acknowledged"
    TERMINATEDWITHERROR  = "terminatedWithError"
    INPROGRESS  = "inProgress"
    DONE_ABANDONED  = "done.abandoned"
    DONE_READY  = "done.ready"

class MEFPOQItemStateChange(BaseModel):
    """Holds information about a change in the state of a POQ item."""
    changeReason: Optional[str] = Field(default="", description="Additional comment related to state change")
    changeDate: datetime = Field( description="The date on when the state was reached")
    state: MEFPOQItemTaskStateType = Field(description="A state which was reached at change date")
    
class ProductOfferingQualificationItem(ProductOfferingQualificationItem_Create):
    '''An individual article included in a POQ that describes a Product of a particular type (Product Offering) being delivered to a specific geographical location.
        The objective is to determine if it is feasible for the Seller to deliver this item as described and for the Seller to inform the Buyer of the estimated time interval to complete this delivery.
        Reference: MEF 79 (Sn 8.4.3.1)
    '''
    terminationError: Optional[List[TerminationError]] = Field(default=None)
    serviceabilityConfidence: Optional[MEFServiceabilityColor] = Field(default=None)
    serviceabilityConfidenceReason: Optional[str] =Field(default="",description = "A free text description of the reason a particular color is being provided.")
    alternateProductOfferingProposal: Optional[List[AlternateProductOfferingProposal]] = Field(
    default = None, description="A list of one or more alternative Product Offerings that the Seller is proposing to the Buyer."
        "If 1) the Buyer has set provideAlternate=true;"
        "2) the Seller has determined that the POQ Confidence Level for this item is yellow or red; and "
        "3) The Seller has alternate Products (e.g. similar but lower bandwidth) that may be adequate. MUST NOT be specified if 'state' is 'terminatedWithError' or 'done.abandoned'"
        )
    installationInterval: Optional[Duration] = Field(default=None)
    guaranteedUntilDate: Optional[datetime] = Field(default=None,description="Date until the Seller guarantees the qualification result. MUST NOT be specified if ")
    stateChange: Optional[List[MEFPOQItemStateChange]] = Field(default=None,description="A log of all state transitions for the POQ Item. It must be in sync with the most recent POQ Item's state.")
    state: MEFPOQItemTaskStateType
    
class ProductOfferingQualification(BaseModel):
    '''
    Represents a response to the Buyer POQ inquiry. This type defines a set of attributes that are assigned by the Seller while processing the request.
    A POQ response is a combination of attributes defined here with common attributes that are sent in the request.
    This type is used in response to an immediate request and POQ retrieval by an identifier. Reference MEF 79 (Sn 8.7 and 8.4.3).
    '''
    externalId: Optional[str] = Field(default="", description = "ID given by the consumer and only understandable by him (to facilitate his searches afterwards)")
    instantSyncQualification: Optional[bool] = Field(default = False, description = "If this flag is set to Yes, Buyer requests to have an instant qualification to be provided in operation POST response")
    relatedContactInformation: List[RelatedContactInformation] = Field(description= "Party playing a role for this qualification. MEF 79 mandates providing 'Buyer Contact Information' in the request ('role=buyerContactInformation') and 'Seller Contact Information' in the response ('role=sellerContactInformation')")
    provideAlternative: Optional[bool] = Field(default=False ,description="Allows the Buyer to indicate if he is willing to get an alternate proposal if requested product not available.")
    projectId: Optional[str] = Field(default="",description="This value MAY be assigned by the Buyer to identify a project the serviceability request is associated with.")
    requestedPOQCompletionDate: Optional[datetime] = Field(default=None, description="The latest date a the POQ completion is expected. This attribute is required when instantSyncQualification=false")
    productOfferingQualificationItem: List[ProductOfferingQualificationItem] = Field(description="One or more of Product Offering Qualification Items. It MUST contain exactly one entry for each item in the POQ request.")
    effectiveQualificationDate: Optional[str] =Field(default = None, description="Date and time (set by the Seller) when the POQ state was set to one of the completion states (done.ready, done.unable_to_provide, terminated_with_error). The Seller MUST NOT provide this attribute until mentioned states are achieved.",
                                                     format="date-time")
    expectedPOQCompletionDate: Optional[str] = Field(default = None, description = "The date the Seller expects to provide qualification result. Set by the Seller in case of providing a deferred response when the POQ is in an acknowledged or inProgress state.",
                                                     format="date-time")
    stateChange: Optional[List[MEFPOQItemStateChange]] = Field(default = None, description="A log of all state transitions for the POQ. It must be in sync with the most recent POQ Request state.")
    href: Optional[str] = Field(default="", description = "Hyperlink to this POQ. Hyperlink MAY be used by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request.")
    id: str =Field(description="The Serviceability Request's unique identifier assigned by the Seller.", 
        min_length=1)
    state: MEFPOQTaskStateType
