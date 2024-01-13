from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, StrictInt, validator

class Interval(str, Enum):
    TEN_MILLISECONDS     = '10 milliseconds'
    HUNDRED_MILLISECONDS = '100 MILLISECONDS'
    ONE_SECOND           = '1 second'
    TEN_SECONDS          = '10 second'
    ONE_MINUTE           = '1 minute'
    FIVE_MINUTES         = '5 minutes'
    FIFTEN_MINUTES       = '15 minutes'
    THIRTY_MINUTES       = '30 minutes'
    ONE_HOUR             = '1 hour'
    TWENTY_FOUR_HOURS    = '24 hours'
    ONE_MONTH            = '1 month'
    ONE_YEAR             = '1 year'
    NOT_APPLICABLE       = 'not applicable'
    
class JobType(str, Enum):
    '''
        The type of PM Job
    '''
    PROACTIVE = 'proactive'
    ON_DEMAND = 'on-demand'
    PASSIVE   =  'passive'
    
class OutputFormat(str, Enum):
    '''
    List of possible output formats for the Performance Report
    '''
    JSON = 'json'
    XML  = 'xml'
    AVRO = 'avro'
    CSV  = 'csv'
    
class ReportingperiodEnum(str, Enum):
    TEN_MILLISECONDS     = '10 milliseconds'
    HUNDRED_MILLISECONDS = '100 milliseconds'
    ONE_SECOND           = '1 second'
    TEN_SECONDS          = '10 second'
    ONE_MINUTE           = '1 minute'
    FIVE_MINUTES         = '5 minutes'
    FIFTEN_MINUTES       = '15 minutes'
    THIRTY_MINUTES       = '30 minutes'
    ONE_HOUR             = '1 hour'
    TWENTY_FOUR_HOURS    = '24 hours'
    
class ResultFormat(str, Enum):
    '''
    List of possible result formats that define how Seller/Server will deliver Performance Report to the Buyer/Client.
    '''
    PAYLOAD    = 'payload'
    ATTACHMENT = 'attachment'
    

class PerformanceProfile_Common(BaseModel):
    
    '''
    A Performance Monitoring Job specifies the performance monitoring objectives specific to each subject of monitoring which could be an ordered pair (i.e., two UNIs) or an entity (i.e., port). 
    '''
    
    buyerProfileId : Optional[str] = Field(default="", description='Identifier of the profile understood and assigned by the Buyer/Client.')
    description    : Optional[str] = Field(default="", description='A free-text description of the Performance.')
    granularity    : Optional[Interval] = Field(default="", description='Sampling rate of the collection or production of performance indicators.')
    jobPriority    : Optional[StrictInt] = Field(default=5,ge=1,le=10,description='The priority of the Performance Job. The way the management application will use the Job priority to schedule Job execution is application specific and out the scope.')
    jobType        : JobType = Field(description='The type of PM Job.')
    outputFormat   : OutputFormat = Field(description='List of possible output formats for the Performance Report.')
    reportingPeriod : Optional[ReportingperiodEnum] = Field(default="",description='Defines the interval for the report generation.')
    resultFormat    : ResultFormat = Field(description='List of possible result formats that define how Seller/Server will deliver Performance Report to the Buyer/Client.')

class Error(BaseModel):
    '''
    Text that provides mode details and corrective actions related to
    the error. This can be shown to a client user.
    '''
    
    message         : Optional[str] = Field(default=None,description = 'Text that provides mode details and corrective actions related to the error. This can be shown to a client user.')
    reason          : str = Field(max_length = 255,description = 'Text that explains the reason for the error. This can be shown to a client user.')
    referenceError  : Optional[HttpUrl] = Field(default=None,description = 'URL pointing to documentation describing the error.')
    

class ReportingTimeframe(BaseModel):
    '''	
    Specifies the date range between which data points will be included in the report.
    '''
    reportingStartDate : datetime
    reportingEndDate   : datetime 


class PerformanceReport_Common(BaseModel):
    '''
    The execution of PM Job results in Performance Measurement collections that provide Buyer/Client with performance objectives results.
    '''
    description        : Optional[str] = Field(default="",description='A free-text description of the performance report.')
    reportingTimeframe : Optional[ReportingTimeframe]

class Event(BaseModel):
    '''
    Event class is used to describe information structure used for
    notification.
    '''
    
    eventId : str =  Field(min_length = 1, description = 'Id of the event.')
    eventTime : datetime = Field(format="date-time",
    description = 'Date-time when the event occurred.')



class MonthlyScheduleDayOfWeekDefinition(BaseModel):
    '''
    Monthly scheduled day of week.
    '''
    recurringDaySequence : Optional[List[int]] = Field(default=[7], description="Day of the week for recurrence. 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday.")
    dayOfMonthRecurrence : Optional[List[int]] = Field(default=[31], description="Day of the month for recurrence.")
    @validator("recurringDaySequence", each_item=True, pre=True, allow_reuse=True)
    def greater_than_or_equal_validator(cls, value):
        le = 1
        ge = 7
        if not (le <= value <= ge):
            raise ValueError(f"Each item in the list must be greater than or equal to {ge} and less than or equal to {le}")
        
        return value
    
    @validator("dayOfMonthRecurrence", each_item=True, pre=True, allow_reuse=True)
    def greater_than_or_equal_validator_dayofmonth(cls, value):
        ge = 31
        le = 1
        if not (le <= value <= ge):
            raise ValueError(f"Each item in the list must be greater than or equal to {ge} or less than or equal to {le}")
        
        return value


class RecurringFrequencyUnits(str, Enum):
    MINUTES = "MINUTES"
    HOURS   = "HOURS"
    DAYS    =  "DAYS"
    WEEKS   = "WEEKS"
    MONTHS  = "MONTHS"


class RecurringFrequency(BaseModel):
    recurringFrequencyValue : int = Field(description="The value of the recurrence as an integer. For example, if the recurring frequency is 2 weeks this value is 2." )
    recurringFrequencyUnits : RecurringFrequencyUnits = Field(description="The unit of measure in recurring frequency. For example, if a recurring frequency is 2 weeks this value is WEEKS." )

class ScheduleDefinitionHourRange(BaseModel):
    start : Optional[str] = Field(default=None, format="date-time")
    end : Optional[str] = Field(default=None, format="date-time")

class ScheduleDefinition(BaseModel):
    '''
    The schedule definition for running jobs.
    '''
    scheduleDefinitionStartTime : Optional[datetime] = Field(default=None, format="date-time", description="The Starttime of the Schedule Definition. If the attribute is empty the Schedule starts immediately after provisioning of the Job.")
    scheduleDefinitionEndTime : Optional[datetime] = Field(default=None, format="date-time", description="The Endtime of the Schedule Definition. If the attribute is empty the Schedule runs forever, not having a time constraint.")
    recurringFrequency : Optional[RecurringFrequency] = Field(default=None)
    scheduleDefinitionHourRange : Optional[List[ScheduleDefinitionHourRange]] = Field(default=None, description="A list of time ranges within a specific day that the schedule will be active on, for example 08:00-12:00, 16:00-19:00." )
    monthlyScheduleDayOfWeekDefinition : Optional[MonthlyScheduleDayOfWeekDefinition]  = Field(default=None)
    weeklyScheduledDefinition : Optional[List[int]] = Field(default=[7], description="The weekly schedule is used to define a schedule that is based on the days of the week, e.g. a schedule that will be active only on Monday and Tuesday.")
    @validator("weeklyScheduledDefinition", each_item=True, pre=True, allow_reuse=True)
    def greater_than_or_equal_validator(cls, value):
        le = 1
        ge = 7
        if not (le <= value <= ge):
            raise ValueError(f"Each item in the list must be greater than or equal to {ge} and less than or equal to {le}")
        return value

class PerformanceProfileRefOrValue(BaseModel):
    '''
    Defines the reference to Performance Monitoring Profile or defines values
    from PerformanceProfile type.
    '''
    type: str = Field(
        alias="@type", 
        example="PerformanceProfileRef", 
        description="This field is used as a discriminator to differentiate if object relates directly to Performance Profile entity or defines values from PerformanceProfile type." 
    )

class ServicePayloadSpecificAttributes(BaseModel):
    """
    ServicePayloadSpecificAttributes is used as an extension point for MEF
    specific service performance monitoring configuration. It includes definition of
    service/entity and applicable performance monitoring objectives. The @type attribute is used
    as a discriminator.
    """
    type: str = Field( 
        alias="@type", 
        description="The name that uniquely identifies type of performance monitoring configuration that specifies PM objectives. In case of MEF services this is the URN provided in performance monitoring configuration specification. The named type must be a subclass of ServicePayloadSpecificAttributes."
    )

class CompressionType(str, Enum):
    NO_PACKING = "NO_PACKING"
    GZIP  = "GZIP"
    TAR = "TAR"
    VEN_DOR_EXT = "VEN-DOR_EXT"
    MI_NOR_EXT = "MI-NOR_EXT"

class FileTransferData(BaseModel):
    '''Defines place where the report content should be stored.'''

    fileFormat : Optional[str] = Field(default="", description="Format of the file containing collected data.")
    fileLocation : Optional[HttpUrl] = Field(default="", description="Location of the file containing collected data.")
    transportProtocol : Optional[str] = Field(default="", description="Transport protocol to use for file transfer.")
    compressionType : Optional[CompressionType] = Field(default="", description="Compression types used for the collected data file.")
    packingType : Optional[str] = Field(default="", description="Specify if the data file is to be packed.")
    retentionPeriod : Optional[str] = Field(default="", description="A time interval to retain the file.")

class PerformanceJob_Create(BaseModel):
    '''
    A Performance Monitoring Job specifies the performance monitoring
    objectives specific to each subject of monitoring which could be an ordered pair (i.e., two
    122 / 162 UNIs) or an entity (i.e., port).
    '''
    buyerJobId : Optional[str] = Field(default="", description="Identifier of the job understoo =d and assigned by the Buyer/Client.")
    consumingApplicationId : Optional[str] = Field(default="", description="Identifier of consuming application.")
    description : Optional[str] = Field(default="", description="A free-text description of the Performance Job.")
    fileTransferData : Optional[FileTransferData] = Field(default=None)
    performanceProfile : PerformanceProfileRefOrValue
    producingApplicationId : Optional[str] = Field(default="", description="Identifier of producing application")
    scheduleDefinition : Optional[ScheduleDefinition] = Field(default=None)
    servicePayloadSpecificAttributes : ServicePayloadSpecificAttributes
    
