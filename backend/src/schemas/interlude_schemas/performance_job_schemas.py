from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from typing import Optional, List
from datetime import datetime
from .performance_profile_schema import PerformanceJobStateType


from .common_schemas import (PerformanceJob_Create)

class PerformanceJob(PerformanceJob_Create):
    creationDate : datetime = Field(description="Date when Performance Job was created." )
    href         : Optional[HttpUrl] = Field(default="", description="Hyperlink reference" )
    id           : str  = Field(description="Unique identifier")
    lastModifiedDate : Optional[datetime] = Field(default=None, description="Date when job was last modified.") 
    rejectionReason : Optional[str] = Field(default="", description="Reason in case creation request was rejected.")
    state  : PerformanceJobStateType
    