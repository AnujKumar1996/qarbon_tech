from pydantic import Field,BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from typing import List, Optional
from src.schemas.sonata_schemas.appointment_schemas import MEFByteSize,WorkOrderRef
from .common_schemas import Note, RelatedContactInformation ,MEFBuyerSellerType,Event
from pydantic import BaseModel, Field, HttpUrl


class AttachmentValue(BaseModel):
    
    """
    Complements the description of an element (for instance a product) through video, pictures.
    """
    attachmentId:Optional[str] =Field(default="", description="locally unique identifier to distinguish items from the Attachment list.")
    author      :str =Field( description="Author of the attechment",min_length=1)
    content     :Optional[str] =Field(default="", description="The actual contents of the attachment object, if embedded, encoded as base64. Either url or (content and mimeType) attributes MUST be provided during creation.") 
    creationDate:datetime =Field(description="The date the Attachment was added")
    description :Optional[str] =Field(default="", description="A narrative text describing the content of the attachment")
    mimeType    :Optional[str] =Field(default="", description="Attachment mime type such as extension file for video, picture and document")
    name        :str =Field( description="The name of the attachment ")
    size        :Optional[MEFByteSize] =Field(default=None)
    source      :MEFBuyerSellerType = Field(description="An enumeration with buyer and seller values.")
    url         :Optional[str]=Field(default="", description="URL where the attachment is located. Either url or (content and mimeType) attributes MUST be provided during creation")

class MEFObservedImpactType(str,Enum):
    """
    An enumeration of the possible values of impact observed by the Buyer.
        degraded: When the Product is impacted and not meeting the Product specifications.
        intermittent: When the Product is not operational as intended on an intermittent basis.
        down: When the Product is non-operational.
    """
    DEGRADED = "degraded"
    INTERMITTENT = "intermittent"
    DOWN = "down"
    
class TroubleTicketPriorityType(str,Enum):
    """
    Possible values for the priority of the Trouble Ticket
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
class RelatedEntity(BaseModel):
    """
    A reference to an entity, where the type of the entity is not known in advance
    """
    referredType: str = Field(
        description="The actual type of the target instance when needed for disambiguation.",
         alias="@referredType",
        )
    href: Optional[str] = Field(
        default="",
        description="Reference of the related entity"
    )
    id: str = Field(
        description="Unique identifier of a related entity."
        )
    role: str = Field(
        description="The role of an entity."
    )    
    
class IssueRelationship(BaseModel):
    """
    Represents relationships to other Trouble Tickets and Incidents
    """
    referredType: str = Field(
        description="The type of the referred Issue (Incident or TroubleTicket)",
        alias="@referredType",
        )
    creationDate: datetime =Field(description="The date the relationship was created")
    description: str =Field(description="A description of the reason for the Relation Source to set the relationship")
    href: Optional[str] = Field(
        default="",
        description="Reference of the Trouble Ticket or Incident"
    )
    id: str = Field(
        description="Unique identifier of the referenced Issue (Trouble Ticket od Incident)"
        )
    relationshipType: str = Field(
        description="Type of the Trouble Ticket relationship can be blocks, depends on, duplicates, causes, etc..."
    )
    source: MEFBuyerSellerType

class TroubleTicketSeverityType(str, Enum):
    """
    Possible values for the severity of the Trouble Ticket
    """
    minor = "minor"
    moderate = "moderate"
    significant = "significant"
    extensive = "extensive"    
    
class TroubleTicketType(str, Enum):
    """
    Possible values for the type of the Trouble Ticket:
        assistance: Requesting help for a situation (not a failure) requiring attention that is not categorized.
        information: Buyer is requesting information on the Issue
        installation: Related to installation issue. Provisioning is complete, but Product is not operational.
        maintenance: Any scheduled or non-scheduled maintenance related Issue.  
    """
    assistance = "assistance"
    information = "information"
    installation = "installation"
    maintenance = "maintenance"
        
        
class TroubleTicket_Create(BaseModel):
    """
    A Trouble Ticket is a record of an issue that is created, tracked, and managed by a Trouble Ticket management system The modeling pattern introduces the Common supertype to aggregate attributes that are common to both TroubleTicket and TroubleTicket_Create. 
    It this case the Create type has a subset of attributes of the response type and does not introduce any new, thus the Create type has an empty definition.
    """ 
    attachment:Optional[List[AttachmentValue]] =Field(default=None, description="Attachments to the Ticket, such as a file, screenshot or embedded content. Attachments may be added but may not be modified or deleted (for historical reasons).")
    description :str =Field(description="Summarized description of the Issue the Buyer is experiencing.")
    externalId :Optional[str] = Field(default="",description="Identifier provided by the Buyer to allow the Buyer to use as a search attribute in Retrieve Ticket List.")   
    issueStartDate:Optional[datetime] = Field(default=None, description="The date indicating when the Buyer first observed the Issue, to provide the Seller with additional insight.")
    note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
    observedImpact:	MEFObservedImpactType
    priority:	TroubleTicketPriorityType
    relatedContactInformation : List[RelatedContactInformation] = Field(
        description= "Party playing a role for this Trouble Ticket. The 'role' is to specify the type of contact \
            as specified in MEF 113: Reporter Contact ('role=reporterContact') - REQUIRED in the request Buyer Technical Contacts ('role=buyerTechnicalContact')\
            Seller Ticket Contact ('role=sellerTicketContact') Seller Technical Contact ('role=sellerTechnicalContact')")
    relatedEntity : List[RelatedEntity] = Field(
        description= "An entity that is related to the ticket such as a bill, a product, etc. The entity against which the ticket is associated.",min_items=1, max_items=1)
    
    relatedIssue : Optional[List[IssueRelationship]] = Field(default=None,
        description= "A list of Related Issue relationships. Represents relationships to other Trouble Tickets and Incidents.")
    
    severity: 	TroubleTicketSeverityType
    ticketType: TroubleTicketType
    
   
class TroubleTicketStatusType(str, Enum):
    """
    Possible values for the status of the Trouble Ticket

    | state                  | MEF 57.2 name           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
    | ---------------------  | -------------           | -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | acknowledged           | ACKNOWLEDGED            | A request to create a Ticket was received and accepted by the Seller. The Ticket create request has been validated and a Ticket has been created by the Seller and allocated a unique id.                                                                                                                                                                                                                                                                                                                        |
    | assessingCancellation  | ASSESSING_CANCELLATION  | A request has been made by the Buyer to cancel the Ticket and is being assessed by the Seller to determine whether to just close the Ticket, or continue to resolve the Issue to prevent similar Create Ticket requests from other Buyers. If the Seller chooses to resolve the Issue, the Seller might create an Incident or an internal Ticket for the Issue, but that is outside the scope of this document. After the Seller has completed the assessment, the Seller updates the Ticket State to cancelled. |
    | cancelled              | CANCELLED               | The Ticket has been successfully cancelled by the Buy-er. The Buyer will receive no further Event Notifications for the Ticket. This is a terminal state.                                                                                                                                                                                                                                                                                                                                                        |
    | closed                 | CLOSED                  | The Buyer has confirmed that the Issue they reported is no longer observed, or the pre-defined time frame (agreed upon between Buyer and Seller) for confirming that the Issue has been resolved has passed without a response by the Buyer. This is a terminal state.                                                                                                                                                                                                                                           |
    | inProgress             | IN_PROGRESS             | The Ticket is in the process of being handled and investigated for resolution by the Seller.                                                                                                                                                                                                                                                                                                                                                                                                                     |
    | pending                | PENDING                 | The Seller is waiting on the Buyer to provide additional information for the Ticket, or the Buyer to schedule an Appointment for the WorkOrder (linked to the Ticket) in order to continue processing the Ticket. This may result in the clock being stopped for the service level agreement until the Buyer has responded to the request                                                                                                                                                                        |
    | reopened               | REOPENED                | The Buyer has verified that the Issue described in the Ticket is still observed and has not been resolved satisfactorily. The Buyer rejects the Seller's request to close the Ticket. The Ticket has been reopened and is waiting for further actions from the Seller.                                                                                                                                                                                                                                           |               
    | resolved               | RESOLVED                | The Buyer's Issue described in the Ticket was resolved by the Seller. The Seller assumes that normal operation is re-established for the Buyer's product and i snow waiting for the Buyer to confirm that the Issue they reported is no longer observed.                                                                                                                                                                                                                                                         |            
    """
    acknowledged = "acknowledged"
    assessingCancellation = "assessingCancellation"
    cancelled = "cancelled"
    closed = "closed"
    inProgress = "inProgress"
    pending = "pending"
    resolved = "resolved"
    reopened = "reopened"
    
class TroubleTicketStatusChange(BaseModel):
    """
    Holds the status notification reasons and associated date the status changed, populated by the serve
    """
    changeDate: Optional[datetime] = Field(default=None,description="The date and time the status changed.")  
    changeDate: Optional[str] = Field(default="",description="The reason why the status changed.") 
    status: TroubleTicketStatusType    
    
class TroubleTicket(BaseModel):
    """
    A Trouble Ticket is a record of an issue that is created, tracked, and managed by a Trouble Ticket management system
    """ 
    attachment:Optional[List[AttachmentValue]] =Field(default=None, description="Attachments to the Ticket, such as a file, screenshot or embedded content. Attachments may be added but may not be modified or deleted (for historical reasons).")
    description :str =Field(description="Summarized description of the Issue the Buyer is experiencing.")
    externalId :Optional[str] = Field(default="",description="Identifier provided by the Buyer to allow the Buyer to use as a search attribute in Retrieve Ticket List.")   
    issueStartDate:Optional[datetime] = Field(default=None, description="The date indicating when the Buyer first observed the Issue, to provide the Seller with additional insight.")
    note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
    observedImpact:	MEFObservedImpactType
    priority:	TroubleTicketPriorityType
    relatedContactInformation : List[RelatedContactInformation] = Field(
        description= "Party playing a role for this Trouble Ticket. The 'role' is to specify the type of contact \
            as specified in MEF 113: Reporter Contact ('role=reporterContact') - REQUIRED in the request Buyer Technical Contacts ('role=buyerTechnicalContact')\
            Seller Ticket Contact ('role=sellerTicketContact') Seller Technical Contact ('role=sellerTechnicalContact')")
    relatedEntity : List[RelatedEntity] = Field(
        description= "An entity that is related to the ticket such as a bill, a product, etc. The entity against which the ticket is associated.",min_items=1, max_items=1)
    
    relatedIssue : Optional[List[IssueRelationship]] = Field( default= None,
        description= "A list of Related Issue relationships. Represents relationships to other Trouble Tickets and Incidents.")
    
    severity: 	TroubleTicketSeverityType
    ticketType: TroubleTicketType
    creationDate: datetime =Field(description="The date on which the Trouble Ticket was created")
    expectedResolutionDate: Optional[datetime] =Field(default=None, description="The date on which the Trouble Ticket was created")
    href: Optional[str] = Field(
        default="",
        description="Hyperlink, a reference to the Trouble Ticket entity"
    )
    id: str = Field(
        description="Unique (within the Seller Ticket domain) identifier for the Ticket."
        )
    resolutionDate: Optional[datetime] =Field(default=None, description="The date the Ticket status was set to resolved by the Seller")
    sellerPriority:	TroubleTicketPriorityType
    sellerSeverity:	TroubleTicketSeverityType
    status: TroubleTicketStatusType
    statusChange: Optional[List[TroubleTicketStatusChange]] =Field(default=None ,description="The status change history that is associated to the ticket. Populated by the Seller.")
    workOrder: Optional[List[WorkOrderRef]] =Field(default=None ,description="A reference to a set of WorkOrders to be performed under the responsibility of Seller technician(s) to resolve the Ticket.")
    
    
class TroubleTicket_Find(BaseModel):
    """
    This class represents a single list item for the response of listTroubleTicket operation.
    """
    creationDate:datetime =Field(description="The date on which the Trouble Ticket was create")
    description :str =Field(description="Summarized description of the Issue the Buyer is experiencing.")
    expectedResolutionDate: datetime =Field(description="The date provided by the Seller to indicate when the Ticket is expected to be resolved")
    externalId :str = Field(description="Additional identifier coming from an external system")   
    id: str = Field(description="Unique identifier of the Trouble Ticket")
    priority:	TroubleTicketPriorityType
    relatedEntity : List[RelatedEntity] = Field(
        description= "An entity that is related to the ticket such as a bill, a product, etc. The entity against which the ticket is associated.",min_items=1, max_items=1)
    observedImpact:	MEFObservedImpactType
    resolutionDate: datetime =Field(description="The date the Ticket status was set to resolved by the Seller")
    sellerPriority:	TroubleTicketPriorityType
    sellerSeverity:	TroubleTicketSeverityType
    severity: 	TroubleTicketSeverityType
    status: TroubleTicketStatusType
    ticketType: TroubleTicketType

class TroubleTicketEventType(str , Enum):
    """
    Type of the Trouble Ticket event.

    | API name                                    | 	MEF 113 name        | Description                                                                                                                                                                                                                                                                                                            |
    | --------------------------------------------|------------------------ | -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | troubleTicketAttributeValueChangeEvent      | TICKET_UPDATE           | The Seller settable attributes for a Ticket were updated by the Seller. Note: Buyer initiated Ticket updates due to Patch operation will not trigger a troubleTicketAttributeValueChangeEvent                                                                                                                          |
    | troubleTicketResolvedEvent                  | TICKET_INFO_REQUIRED    | The Seller requires more information from the Buyer for a Ticket to continue processing a Ticket. The details on what information is needed from the Buyer will be provided via a Ticket note. The Ticket status is pending. Note: The Buyer uses the Patch operation to provide more information for a Ticket.        |
    | troubleTicketStatusChangeEvent              | TICKET_RESOLVED         | 	The Seller is informing the Buyer the Ticket is resolved and the Buyer to verify that the Issue on which the Ticket was based is no longer observed. The Ticket status is resolved. Note: The Buyer confirms if the Issue has been resolved satisfactorily or not using close or reopen operations                   |
    """
    TICKET_UPDATE = "troubleTicketAttributeValueChangeEvent"
    TICKET_STATE_CHANGE = "troubleTicketInformationRequiredEvent"
    TICKET_INFO_REQUIRED = "troubleTicketResolvedEvent"
    TICKET_RESOLVED = "troubleTicketStatusChangeEvent"
    
class TroubleTicket_Update(BaseModel):
    """   
    A Trouble Ticket is a record of an issue that is created, tracked, and managed by a Trouble Ticket management system 
    """   
    attachment:Optional[List[AttachmentValue]] =Field(default=None, description="Attachments to the Ticket, such as a file, screenshot or embedded content. Attachments may be added but may not be modified or deleted (for historical reasons).")
    externalId :Optional[str] = Field(default="",description="Identifier provided by the Buyer to allow the Buyer to use as a search attribute in Retrieve Ticket List.")   
    issueStartDate:Optional[datetime] = Field(default=None, description="The date indicating when the Buyer first observed the Issue, to provide the Seller with additional insight.")
    observedImpact:	Optional[MEFObservedImpactType] = Field (default=None)
    note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
    priority:	Optional[TroubleTicketPriorityType] = Field (default=None)
    relatedContactInformation : Optional[List[RelatedContactInformation]] = Field( default=None,
        description= "Party playing a role for this quote. If instantSyncQuote=false then the Buyer MUST specify Buyer Contact Information ('role=buyerContactInformation') and the Seller MUST specify Seller Contact Information ('role=sellerContactInformation')")
    relatedIssue : Optional[List[IssueRelationship]] = Field( default = None,
        description= "A list of Related Issue relationships. Represents relationships to other Trouble Tickets and Incidents.")
    severity: 	Optional[TroubleTicketSeverityType] = Field(default = None)
    
    
   
class TroubleTicketEventPayload(BaseModel):
    '''
    The identifier of the Trouble Ticket being subject of this event.
    '''
    sellerId: Optional[str] = Field(default = "", description = "The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when requester entity represents more than one Seller.")
    id: str = Field(description = "ID of the Trouble Ticket attributed by quoting system")
    href: Optional[str] = Field (default = "", description = "Hyperlink to access the Trouble Ticket")
    buyerId: Optional[str] = Field(default = "", description  = "The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")
    
class TroubleTicketEvent(Event):
    """
    Event class is used to describe information structure used for notification
    """
    eventType: TroubleTicketEventType
    event: TroubleTicketEventPayload
    
class Reason(BaseModel):
    """
    An object to convey a reason for the operation.
    """
    reason:str = Field(description="A text description of why given operation was requested.")