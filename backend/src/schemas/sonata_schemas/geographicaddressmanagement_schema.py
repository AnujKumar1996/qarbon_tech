

from pydantic import BaseModel, Field
from typing import  Optional
from .common_schemas import FieldedAddress
from enum import Enum


class GeographicAddress(BaseModel):
    
    """
    Structured textual way of describing how to find a property in an urban area (country properties are often defined differently).
    Note: Address corresponds to SID UrbanPropertyAddress
    """
    hasPublicSite :Optional[bool] =Field(default=False, description="This attribute specifies if that Address contains Service Sites that are public such as Meet-Me-Rooms at an interconnect location or a shared telecom room in the basement of a multi-tenant building.")
    type: str = Field(
        alias="@type",
        example="FieldedAddress",
        description="This field is used as discriminator. The value is the name of one of the types that inherit from it using 'allOf', i.e. one of FieldedAddress, FormattedAddress, GeographicAddressLabel, MEFGeographicPoint. Moreover, it might discriminate for an additional related place as defined in '@schemaLocation'."
        )
    allowsNewSite:Optional[bool] =Field(default=False, description="This attribute specifies if a Buyer must use one of the known existing Service Sites at this location for any Products delivered to this Address. For example, if a particular building owner mandated that all interconnects be done in a shared Public Meet-Me-Room, this attribute would be set to False for that Address.")
    id:Optional[str]=Field(default="", description="Unique identifier of the place")
    href: Optional[str] = Field(
        default="",
        description="Unique reference of the place"
        )
    schemaLocation: Optional[str] = Field(
        default=None,
        alias="@schemaLocation",
        description="A URI to a JSON-Schema file that defines additional attributes and relationships.\
            May be used to define additional related place types. Usage of this attribute must be agreed upon\
            between Buyer and Seller.",
        pattern=r'^https?://\S+$'
    )
    
    associatedGeographicAddress:Optional[FieldedAddress] =Field(default=None)
    

class GeographicAddres(BaseModel):
    
    type: str = Field(
        alias="@type",
        example="FieldedAddress",
        description="This field is used as discriminator. The value is the name of one of the types that inherit from it using 'allOf', i.e. one of FieldedAddress, FormattedAddress, GeographicAddressLabel, MEFGeographicPoint. Moreover, it might discriminate for an additional related place as defined in '@schemaLocation'."
        ) 
    schemaLocation: Optional[str] = Field(
        default="",
        alias="@schemaLocation",
        description="A URI to a JSON-Schema file that defines additional attributes and relationships.\
            May be used to define additional related place types. Usage of this attribute must be agreed upon\
            between Buyer and Seller.",
        pattern=r'^https?://\S+$'
    )
    
    associatedGeographicAddress:Optional[FieldedAddress] =Field(default=None) 
class GeographicAddressValidation_Create(BaseModel):
    """
    This resource is used to manage address validation request.
    """ 
    provideAlternative:bool = Field(
                                    description="Indicator provided by the requester to specify if alternate addresses must be provided in case of partial or fail result. MEF: The attribute is kept for TMF API compliance. MEF requires this attribute always to be set to 'true'. Alternatives should be provided regardless of whether best match was found. The Seller is allowed not to implement the support for 'false'.")   
    
    submittedGeographicAddress: GeographicAddres

class MEFValidationResultType(str,Enum):
    """
    Possible values for the Address Validation Result:

    | Value   | Description                                       |
    |---------|---------------------------------------------------|
    | success | Best match found                                  |
    | partial | No best match, but alternatives available         |
    | fail    | Neither best match nor alternatives provided      |
    """  
    SUCCESS  = 'success'
    PARTIAL  = 'partial'
    FAIL     =  'fail' 
             
class GeographicAddressValidation(BaseModel):
    """
    This resource is used to manage address validation response.
    """  
    
    validationResult:Optional[MEFValidationResultType] = Field(default=None) 
    alternateGeographicAddress:Optional[list[GeographicAddress]] = Field(default=None) 
    provideAlternative:bool = Field(default=False ,description="Indicator provided by the requester to specify if alternate addresses must be provided in case of partial or fail result. MEF: The attribute is kept for TMF API compliance. MEF requires this attribute always to be set to 'true'. Alternatives should be provided regardless of whether best match was found. The Seller is allowed not to implement the support for 'false'")
    submittedGeographicAddress:GeographicAddress 
    bestMatchGeographicAddress:Optional[GeographicAddress]  = Field(default=None)
        