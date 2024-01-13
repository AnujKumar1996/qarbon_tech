from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from src.schemas.sonata_schemas.common_schemas import Note
from .common_schemas import  RelatedContactInformation
from src.schemas.sonata_schemas.common_schemas import Event

class RelatedPlaceRefOrValue(BaseModel):
    schemaLocation: Optional[str] = Field(
        default="",
        description="A URI to a JSON-Schema file that defines additional attributes and relationships. \
                    May be used to define additional related place types. Usage of this attribute must be.\
                    agreed upon between Buyer and Seller.",
        alias="@schemaLocation"
    )
    type: str = Field(
        description="This field is used as a discriminator and is used between different place representations.\
                    This type might discriminate for additional related place as defined in '@schemaLocation'.",
        alias="@type"
    )
    role: str = Field(
        description="Role of this place."
    )

class RelatedEntity(BaseModel):
    id: str = Field(
        description="Unique identifier of a related entity."
        )
    referredType: str = Field(
        description="The actual type of the target instance when needed for disambiguation.",
         alias="@referredType",
        )
    href: Optional[str] = Field(
        default="",
        description="Reference to the entity which the WorkOrder is associated with."
    )
    role: str = Field(
        description="The role of an entity."
    )

class TimeDurationUnits(str, Enum):
    """The unit of measure in the duration. For example, if an interval is 2ms, this element is MS."""
    NS = 'ns'
    US = 'us'
    MS = 'ms'
    SEC = 'sec'
    MIN = 'min'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'
    
class WorkOrderStateType(str, Enum):
    """
        | Name               | MEF 113 Name        | Description                                                                                                                                         |
        | ------------------ | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
        | completed          | COMPLETED            | The Seller Technician responsible for the WorkOrder has successfully completed all the assigned Tasks.                                               |
        | cancelled          | CANCELLED            | The WorkOrder has been cancelled by the Seller or due to the Buyer requesting to cancel the WorkOrder.                                                 |
        | inProgress         | IN_PROGRESS          | The Seller Technician responsible for the WorkOrder has been assigned and started one or more of the assigned Tasks.                                   |
        | open               | OPEN                 | A WorkOrder was initiated by the Seller to be assigned to a Technician responsible for resolving the WorkOrder.                                       |
        | planned            | PLANNED              | The WorkOrder has been given an execution date for resolving one or more Tasks.                                                                         |
        | unableToComplete   | UNABLE_TO_COMPLETE   | The Seller Technician responsible for the WorkOrder was unable to complete one or more of the assigned Tasks, because additional skills or information is required. Additional tasks are required to resolve the WorkOrder and a new WorkOrder needs to be opened. |
    """
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    IN_PROGRESS = 'inProgress'
    OPEN = 'open'
    PLANNED = 'planned'
    UNABLE_TO_COMPLETE = 'unableToComplete'
    


class WorkOrder_Find(BaseModel):
    id: str = Field(
        description="Unique (within the Seller domain) identifier for the WorkOrder."
    )
    appointmentRequired: bool = Field(
        description="Indicates if the Seller requires the Buyer to schedule an Appointment."
    )
    place: List[RelatedPlaceRefOrValue] = Field(
        description="The location where the WorkOrder Tasks are to be performed. If an appointment is needed, this will also be the location where the Appointment takes place and includes the site contact which the Seller technician may need to get access to the Buyer's site during the Appointment. This could be an end-user, security personnel or any authorized person."
    )
    relatedEntity: List[RelatedEntity] = Field(
        description="An entity that is related to the WorkOrder, such as a service, a product, etc."
    )
    state: WorkOrderStateType = Field(
        description="The current state of the WorkOrder."
    )


class AppointmentRef(BaseModel):
    '''	
    A reference to an Appointment resource available through Appointment API.
    ''' 
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to the referenced Appointment. Hyperlink MAY be used by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request"
    )
    id: str = Field(
        description="Identifier of the referenced Appointment."
    )

class 	TimeDuration(BaseModel):
    '''	
    A reference to an Appointment resource available through Appointment API.
    '''
    timeDurationValue: int = Field(
        description="Hyperlink to the referenced Appointment. Hyperlink MAY be used by the Seller in responses. Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request"
    )
    timeDurationUnits: TimeDurationUnits = Field(
        description="The unit of measure in the duration. For example, if an interval is 2ms, this element is MS."
    )


class WorkOrder(WorkOrder_Find):
    '''	
    A set of tasks to be scheduled and performed under the responsibility of a Seller Technician(s)
    '''
    href: Optional[str] = Field(
        default="",
        description="Hyperlink, a reference to the WorkOrder entity."
    )
    appointment: Optional[List[AppointmentRef]] = Field(
        default= None,
        description= "A reference to a set of Appointments for the WorkOrder. A WorkOrder may contain only one open Appointment at a time (e.g. with the state of 'scheduled')."
    )
    duration: TimeDuration = Field(
        description= "This class is used to describe durations expressed as a 2-tuple, (value, units). The units from nanoseconds to years."
    )
    note: Optional[List[Note]]  = Field(
        default = None,
        description= "A set of unstructured comments or information associated to the WorkOrder"
    )
    plannedExecutionDate: Optional[str]  = Field(
        default = None, 
        description= "The date provided by the Seller to indicate when the Workorder is expected to be started.",
        format="data_time"
    )
    relatedContactInformation : List[RelatedContactInformation] = Field(
    description= "Party playing a role in this WorkOrder. \
                The 'role' is to specify the type of contact as specified in MEF 113: Technical Contact ('role=technicalContact') - REQUIRED to be set by the Seller. \
                The Seller technical contact responsible for the WorkOrder. Technician ('role=technician') - The Seller technician assigned to the WorkOrder and responsible for performing a set of tasks.\
                In certain instances this could be a Buyer technician that works on behalf of the Seller.")
    task: List[str] = Field(
        description= "A set of tasks to be performed under the responsibility of the Technician to fulfil the WorkOrder. \
                    Each item is a description of a specific task to be performed under the responsibility of the Technician."
    )

class WorkOrderEventType(str, Enum):
    '''Type of the WorkOrder Event'''
    WORKORDERCREATEEVENT = 'workOrderCreateEvent'
    WORKORDERSTATECHANGEEVENT  = 'workOrderStateChangeEvent'
    WORKORDERAPPOINTMENTREQUIREDEVENT = 'workOrderAppointmentRequiredEvent'

class WorkOrderEventPayloadWorkOrderEventPayload(BaseModel):
    sellerId: Optional[str] = Field(default = "", description ="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the requester entity represents more than one Seller." )
    id: str = Field(description = "ID of the WorkOrder attributed by quoting system")
    href: Optional[str] = Field(default = "", description = "Hyperlink to access the WorkOrder")
    buyerId: Optional[str] = Field(default = "", description = "The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")
        
class WorkOrderEventWorkOrderEvent(Event):
    
    '''Event class is used to describe the information structure used for notification'''
    eventType: WorkOrderEventType
    event: WorkOrderEventPayloadWorkOrderEventPayload = Field(description = "The identifier of the WorkOrder is subject of this event.")