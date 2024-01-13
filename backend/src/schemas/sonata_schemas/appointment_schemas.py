from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from .common_schemas import Note, RelatedContactInformation ,MEFBuyerSellerType, RelatedPlaceRefOrValue
from datetime import datetime
from .common_schemas import Event

class DataSizeUnitstring(str,Enum):
    """
    The unit of measure in the data size
    """
    BYTES="BYTES"
    KBYTES="KBYTES"
    MBYTES="MBYTES"
    GBYTES="GBYTES"
    TBYTES="TBYTES"
    PBYTES="PBYTES"
    EBYTES="EBYTES"
    ZBYTES="ZBYTES"
    YBYTES="YBYTES"


class MEFByteSize(BaseModel):
    """
     A size represented by value and Byte units
    """
    amount:Optional[float]= Field(default=1, description="Numeric value in a given unit")
    units:Optional[DataSizeUnitstring] =Field(default="")

class AttachmentValue(BaseModel):
    
    """
    Complements the description of an element (for instance a product) through video, pictures.
    """
    attachmentId:Optional[str] =Field(default="", description="locally unique identifier to distinguish items from the Attachment list.")
    author      :str =Field( description="Author of the attechment")
    content     :Optional[str] =Field(default="", description="The actual contents of the attachment object, if embedded, encoded as base64. Either url or (content and mimeType) attributes MUST be provided during creation.") 
    creationDate:Optional[datetime] =Field(default=None, description="The date the Attachment was added")
    description :Optional[str] =Field(default="", description="A narrative text describing the content of the attachment")
    mimeType    :Optional[str] =Field(default="", description="Attachment mime type such as extension file for video, picture and document")
    name        :str =Field( description="The name of the attachment ")
    size        :Optional[MEFByteSize] =Field(default=None)
    source      :MEFBuyerSellerType = Field(description="An enumeration with buyer and seller values.")
    url         :Optional[str]=Field(default="", description="URL where the attachment is located. Either url or (content and mimeType) attributes MUST be provided during creation")

class TimePeriod(BaseModel):
    """
    A period of time, either as a deadline (endDateTime only) a startDateTime only, or both
    """
    endDateTime:datetime =Field( description="End of the time period, using IETC-RFC-3339 format")
    startDateTime:datetime =Field( description="Start of the time period, using IETC-RFC-3339 format. If you define a start, you must also define an end")

class WorkOrderRef(BaseModel):
    """
     A reference to an WorkOrder resource.
    """
    href:Optional[str] = Field(default="", description="Hyperlink to the referenced WorkOrder")
    id:str = Field( description='Identifier of the referenced WorkOrder.')
    
class Appointment_Create(BaseModel):
    attachment:Optional[List[AttachmentValue]] = Field(default = None, description="Attachments to the Appointment, such as a file, screen shot or embedded content.")
    note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
    relatedContactInformation:List[RelatedContactInformation]
    validFor:TimePeriod
    workOrder:WorkOrderRef

class AppointmentStatusType(str,Enum):
      CONFIRMED   = "confirmed" 
      IN_PROGRESS = "inProgress"  
      CANCELLED   = "cancelled"
      MISSED      = "missed"
      FAILED      = "failed"
      COMPLETED   = "completed"

class Appointment(BaseModel):
      """  
      In the context of MEF 113 document, denotes an arrangement between the Buyer and Seller for a Seller Technician to meet with the Buyer at a specified time and place.
      """ 
      id :str = Field(description="Unique identifier of the appointment")   
      href:Optional[str] = Field(default="", description="Unique URI used to access to the appointment resource")
      attachment:Optional[List[AttachmentValue]] =Field(default=None, description="Attachments to the Appointment, such as a file, screenshot or embedded content")
      note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
      relatedPlace:	RelatedPlaceRefOrValue
      status:AppointmentStatusType
      validFor:TimePeriod
      relatedContactInformation:List[RelatedContactInformation]
      workOrder:WorkOrderRef



class TimeSlot(BaseModel):
    
    validFor:TimePeriod

   
class SearchTimeSlot_Create(BaseModel):
    
    """
    This task resource is used to retrieve available time slots. One of this available time slot is after used to create or reschedule an appointment.
    """
   
    requestedTimeSlot:List[TimeSlot] =Field(description="A set of preferred time slots the Buyer is requesting the Seller to verify for availability by a Sellers Technician at the Place referenced in the Appointment Related Entity. For example Monday thru Friday, or a set of specific time slots.")
    workOrder :WorkOrderRef

class SearchTimeSlot(BaseModel):

    """
    This task resource is used to retrieve available time slots. One of this available time slot is after used to create or reschedule an appointment.
    """

    availableTimeSlot:List[TimeSlot] =Field(description="A set of time slots with the availability of a Seller Technician returned by the Seller, which the Buyer may select for creating or rescheduling an Appointment.")
    requestedTimeSlot:List[TimeSlot] =Field(description="A set of preferred time slots the Buyer is requesting the Seller to verify for availability by a Sellers Technician at the Place referenced in the Appointment Related Entity. For example Monday thru Friday, or a set of specific time slots.")
    workOrder :WorkOrderRef

      
class Appointment_Find(BaseModel):
    """
    In the context of MEF 113 document, denotes an arrangement between the Buyer and Seller for a Seller Technician to meet with the Buyer at a specified time and place.
    """
    id :str = Field(description="Unique identifier of the appointment")   
    href:Optional[str] = Field(default="", description="Unique URI used to access to the appointment resource")
    relatedPlace:RelatedPlaceRefOrValue
    status:AppointmentStatusType
    validFor:TimePeriod
    workOrder:WorkOrderRef
    
class Appointment_Update(BaseModel):
    
    """
    In the context of MEF 113 document, denotes an arrangement between the Buyer and Seller for a Seller Technician to meet with the Buyer at a specified time and place.
    """
    attachment:Optional[List[AttachmentValue]] =Field(default=None, description="Attachments to the Appointment, such as a file, screenshot or embedded content") 
    note: Optional[List[Note]] = Field(default = None, description="Notes describing the purpose of and the results of the Appointment")
    relatedPlace:Optional[RelatedPlaceRefOrValue] =Field(default=None)
    relatedContactInformation:Optional[List[RelatedContactInformation]] =Field(default=None)
    validFor:Optional[TimePeriod] =Field(default=None)

class AppointmentEventType(str,Enum):
    """
    Type of the Appointment Event
    """
    APPOINTMENT_UPDATE = 'appointmentAttributeValueChangeEvent'
    APPOINTMENT_STATUS_CHANGE = 'appointmentStatusChangeEvent'

class AppointmentEventPayload(BaseModel):
    '''
    The identifier of the Appointment is subject of this event
    '''
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the requester entity represents more than one Seller.")
    id : str = Field(description='ID of the Appointment attributed by quoting system')        
    href : Optional[str] = Field(default="", description='Hyperlink to access the Appointment')
    buyerId : Optional[str] = Field (default="", description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")

class AppointmentEvent(Event):
    '''
    Event class is used to describe the information structure used for notification.
    '''
    eventType : AppointmentEventType 
    event : AppointmentEventPayload
 
