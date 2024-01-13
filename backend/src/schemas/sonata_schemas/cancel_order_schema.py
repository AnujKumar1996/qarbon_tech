from typing import List, Optional
from enum import Enum
from pydantic import Field

from .common_schemas import  MEFProductOrderRef, RelatedContactInformation, MEFProductOrderChargeRef, MEFChargeableTaskStateType
from src.schemas.qcl_cc_schemas.cancel_cross_connect_schemas import QclObject
from pydantic import BaseModel, Field


class CancellationReasonType(str, Enum):
    """
    Identifies the type of reason, Technical or Commercial, for the Cancellation Request

    |  Value            | MEF 57.2   |
    | ----------------- | ---------- |
    | technical         | TECHNICAL  |
    | commercial        | COMMERCIAL |

    """
    TECHNICAL   = 'technical'
    COMMERCIAL  = 'commercial'
    
class CancelProductOrder_Create(QclObject):
    """
    Request for cancellation an existing product order Skipped properties: id,href,state,effectiveCancellationDate
    """
    cancellationReason : str = Field(
        
        description="An optional attribute that allows the Buyer to provide additional detail to the Seller \
            on their reason for cancelling the Product Order",min_length = 5
        )
     
    cancellationReasonType: Optional[CancellationReasonType] = Field(
        default="",
        description="Identifies the type of reason, Technical or Commercial, for the Cancellation request"
        )
    
    productOrder : MEFProductOrderRef = Field(
        description="A reference to a Product Order that the buyer wishes to cancel.")
    
    relatedContactInformation : List[RelatedContactInformation] = Field(
        description= " Contact information of an individual or organization playing a role for this Cancel ProductOrder.\
        The rule for mapping are presented attribute value to a `role` is to use the _lowerCamelCase_ \
            pattern e.g. - Cancel Product Order Contact: `role=cancelProductOrderContact`")
    
class CancelProductOrder(BaseModel):
    '''
    description: Request for cancellation an existing product order
    '''
    
    cancellationDeniedReason : Optional[str] = Field(default="",description="If the Cancel Product Order request is \
        denied by the Seller, the Seller provides a reason to the Buyer using this attribute.")
    
    cancellationReason : str = Field(description="An optional attribute that allows the \
        Buyer to provide additional detail to the Seller on their reason for cancelling the Product Order")
    
    cancellationReasonType : Optional[CancellationReasonType] = Field(default="",description="Identifies the \
        type of reason, Technical or Commercial, for the Cancellation request")
    
    charge : Optional[MEFProductOrderChargeRef] = Field(default=None,description="The Charge Identifier of any charges \
        that are related to the Cancel Product Order.")
    
    href : Optional[str] = Field(default="", description="Hyperlink to the cancellation request. Hyperlink MAY \
        be used by the Seller inresponses Hyperlink MUST be ignored by the Seller in case it is provided by the Buyer in a request")
    
    id : str = Field(description="Unique identifier for the Cancel Product Order that is generated by the Seller \
        when the Cancel Product Order request `state` is set to `acknowledged` ")
    
    productOrder : MEFProductOrderRef = Field(
        description="A reference to a Product Order that the Buyer wishes to cancel.")
    
    relatedContactInformation : List[RelatedContactInformation] = Field(
        description="Contact information of an individual or organization playing a role for this Cancel Product \
            Order. The rule for mapping a represented attribute value to a `role` is to use the _lowerCamelCase_ pattern \
                e.g. - Cancel Product Order Contact: `role=cancelProductOrderContact` - Cancel Product Order \
                    Seller Contact: `role=cancelProductOrderSellerContact")
    
    state : MEFChargeableTaskStateType = Field(description="The states as defined by TMF622 and extended to meet \
        MEF requirements. These states are used to convey the Cancel Product Order status during the lifecycle of the Product Order.")
    
class CancelProductOrder_Find(BaseModel):
    '''
    description: Request for cancellation an existing product order
    '''
    cancellationReasonType : CancellationReasonType = Field(description="Identifies the type of reason, Technical or Commercial, for the Cancellation request")
    id : str = Field(description="Unique identifier for the Cancel Product Order that is generated by the Seller \
        when the Cancel Product Order request `state` is set to `acknowledged` ")
    productOrder : MEFProductOrderRef = Field(description="Holds the MEF Product Order reference")
    state : MEFChargeableTaskStateType = Field( description="The states as defined by TMF622 and extended to meet MEF requirements.")
    