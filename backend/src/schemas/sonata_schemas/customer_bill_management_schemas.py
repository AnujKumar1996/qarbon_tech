from typing import Optional, List
from enum import Enum
from pydantic import Field
from datetime import datetime
from pydantic import BaseModel, Field
from .common_schemas import Event
from .common_schemas import  RelatedContactInformation
from .common_schemas import Event

class BillingAccountRef(BaseModel):
    """
    An identifier for the Billing Account that is unique within the Seller
    """
    id : str = Field(description="Unique-Identifier", min_length=1)

class TimePeriod(BaseModel):
    
    """
    A period of time, either as a deadline (endDateTime only) a startDateTime only, or both.
    """
    endDateTime:Optional[str] = Field(default=None, description="The date the Billing Period ended.",format="date-time")
    startDateTime:Optional[str]  = Field(default=None, description="The date the Billing Period started.",format="date-time" )
class CustomerBillCategory(str, Enum):
    """
    The type of Bill.
    """
    NORMAL = "normal"
    DUPLICATE = "duplicate"
    TRAIL = "trial"

class CustomerBillStateType(str, Enum):
    """
    The state of the Bill.
    """
    GENERATED  = "generated"
    PAYMENTDUE = "paymentDue"
    SETTLED    = "settled"
    
class CustomerBill_Find(BaseModel):
    """
    A legal document generated by the Seller to the Buyer relating to charges associated to Products provided by the Seller to the Buyer.
    """
    id : str = Field(description="An identifier assigned to the Bill by the Seller", min_length=1)
    billingAccount:Optional[BillingAccountRef] = Field(default=None)
    billNo : str = Field(description="A number assigned to the Bill by the Seller.")   
    billingPeriod : Optional[TimePeriod] = Field(default=None)
    category : CustomerBillCategory
    state : CustomerBillStateType

class Money(BaseModel):
    
    """
    A base / value business entity used to represent money
    """ 
    unit: str = Field(description = "Currency (ISO4217 norm uses 3 letters to define the currency)")   
    value: float = Field(description = "A positive floating point number")

class PaymentItem(BaseModel):
    
    """ 
    A payment that has been received. 
    """ 
    id : str = Field(description="An identifier for the payment that is unique within the Buyer Billing Account and is assigned by the Seller.", min_length=1)
    amount : Optional[Money] = Field(default=None)
    paymentMethod: Optional[str] = Field(
        None,
        description="The specific means of payment.",
        enum=["check", "wireTransfer", "electronic", "cash", "other"]
    )
    paymentDate : Optional[str] =Field(default=None, description="The Date the payment was received.", format="date-time")
    
class AppliedPayment(BaseModel):
    
    """ 
    A list of details of a payment that has been received from the Buyer.
    """ 
    appliedAmount :Optional[Money] = Field(default=None)
    payment :Optional[PaymentItem] = Field(default=None)

class BillingAccountRef(BaseModel):
    
    """
    An identifier for the Billing Account that is unique within the Seller
    """
    id : str = Field(description="Unique-Identifier", min_length=1)

class AttachmentURL(BaseModel):
    
    """
    The URL pointing to an Attachment for download.
    """
    url :Optional[str] = Field(default="", description="The URL pointing to an Attachment for download.")

class TimePeriod(BaseModel):
    
    """
    A period of time, either as a deadline (endDateTime only) a startDateTime only, or both
    """
    endDateTime:Optional[str] = Field( description="The date the Billing Period ended.", format="date-time")
    startDateTime:Optional[str] = Field( description="The date the Billing Period started.", format="date-time")

class CustomerBillCategory(str, Enum):
    
    NORMAL = "normal"
    DUPLICATE = "duplicate"
    TRAIL = "trial"
    
class CustomerBillItemRef(BaseModel):
    
    """
    A reference to a Customer Bill resource.
    """ 
    href : Optional[str] = Field(description="Hyperlink to the referenced Customer Bill.") 
    id : str = Field(description="Identifier of the referenced Customer Bill.", min_length=1)  

class FinancialAccountRef(BaseModel):
    
    """
    A Financial Account within the Seller.
    """
    id : str = Field(description="An identifier for the Financial Account that is unique within the Seller and is assigned by the Seller.", min_length=1)
    href : Optional[str] = Field(default="", description="Unique reference of the account.")
    name : Optional[str] = Field(default="", description="The name of the Financial Account.")
    type : Optional[str] = Field(default="", description="The type of the Financial Account.")

class CustomerBillRunType(str,Enum):
    
     """
     The Billing cycle as set by the Seller.
     """ 
     ONCYCLE = "onCycle"
     OFFCYCLE = "offCycle"   

class CustomerBillStateType(str,Enum):
    
    """
    The state of the Bill.
    """
    GENERATED = "generated"
    PAYMENTDUE = "paymentDue"
    SETTLED = "settled"

class TaxItem(BaseModel):
    
     """
     A tax item is created for each tax rate and tax type used in the bill.
     """  
     taxCategory : Optional[str] = Field(default="", description="The Tax Category for this tax item.") 
     taxRate : Optional[float] = Field(default=0.0, description="The Tax Rate for this Tax Item." )
     taxAmount : Money 
class CustomerBill(BaseModel):
    
    """
    A legal document generated by the Seller to the Buyer relating to charges associated to Products provided by the Seller to the Buyer.
    """
    
    id : str = Field(description="An identifier assigned to the Bill by the Seller", min_length=1)
    href :Optional[str] = Field(default="", description="Bill's unique reference.")
    amountDue : Money
    appliedPayment : List[AppliedPayment] =Field(description="A list of details of a payment that has been received from the Buyer.")
    billingAccount : BillingAccountRef 
    billCycle :str = Field( description="The identifier of the Billing Cycle iteration.")
    billDate : str = Field( description="Date the Bill was issued.", format="date-time")
    billDocument : AttachmentURL 
    billNo : str = Field(description="A number assigned to the Bill by the Seller.")
    billingPeriod : TimePeriod
    category : CustomerBillCategory
    credits : Money
    customerBillItem : List[CustomerBillItemRef] =Field(description="A reference to the Bill Items for this Bill.")
    discounts : Money
    fees : Money
    financialAccount : FinancialAccountRef
    lastUpdate : str = Field(description="The date when the Bill was last modified.",format="date-time")
    paymentDueDate : str = Field(description="The date by which payment of the Amount Due must be received by the Seller.",format="date-time")
    runType : CustomerBillRunType
    relatedContactInformation : List[RelatedContactInformation] = Field(description="A party related to this Bill.")
    remainingAmount : Money
    state : CustomerBillStateType
    taxExcludedAmount : Money
    taxIncludedAmount : Money
    taxItem : List[TaxItem] = Field(description="A tax item is created for each tax rate and tax type used in the bill.")

class CustomerBillItemTaxCategory(str,Enum):
    """ 
    The category of the Tax. One of the following:

            country
            state
            county
            city
            other
    """ 
    COUNTRY = "country" 
    STATE = "state"
    COUNTY = "county" 
    CITY = "city"
    OTHER = "other"
    
class CustomerBillItemFeeCategory(str,Enum):
    """
    The category of the Fee. One of the following:

    recurring
    nonRecurring
    other
    """   
    RECURRING = "recurring" 
    NONRECURRING = "nonRecurring"
    OTHER = "other"
class CustomerBillItemTax(BaseModel):
    """ 
    The applied billing tax rate represents the taxes applied billing rate it refers to. It is calculated during the billing process.
    """   
    category : Optional[CustomerBillItemTaxCategory] = Field(default=None)
    description : Optional[str] = Field(default="", description="A description of the type of Tax.")
    rate : Optional[float] = Field(default=0.0, description="The rate at which the Tax is calculated.")
    amount : Optional[Money]
    
class CustomerBillItemFee(BaseModel):
    """ 
    Fees associated with the Bill Item.
    """   
    category : Optional[CustomerBillItemFeeCategory] = Field(default=None)
    description : Optional[str] = Field(default="", description="A description of the type of fee.")
    rate : Optional[float] = Field(default=0.0, description="The rate at which the fee is calculated.")
    amount : Optional[Money]

class MEFPriceType(str,Enum):
    """  
    The type of charge related to the Bill Item.
    """
    RECURRING = "recurring" 
    NONRECURRING = "nonRecurring"
    USAGEBASED = "usageBased"
    
class ProductRef(BaseModel):
    
    id : str = Field(description="Unique identifier of a related entity..", min_length=1)
    href :Optional[str] = Field(default="", description="Reference of the related entity.")   

class MEFProductOrderItemRef(BaseModel):
    """
    It's a ProductOrder item
    """ 
    productOrderHref:Optional[str] = Field(default="", description="Reference of the related ProductOrder.")   
    productOrderId: str = Field(description="Unique identifier of a ProductOrder.", min_length=1)
    productOrderItemId: str = Field(description="Id of an Item within the Product Order", min_length=1)  

class CustomerBillItemStateType(str, Enum):
    """
    The state of the BillItem.
    
    """
    CREDIT = "credit"
    DISPUTEBEINGINVESTIGATED = "disputeBeingInvestigated"
    GENERATED = "generated"
    PAYMENTDUE = "paymentDue"
    SETTLED = "settled"
    WITHDRAWN = "withDrawn"
    
class CustomerBillItem(BaseModel):
    
    """
    One or more rows in a Bill that represent charges associated with a Product instance.
    """ 
    id : str = Field(description="The CustomerBillItem identifier.", min_length=1)
    href :Optional[str] = Field(default="", description="Reference of the CustomerBillItem")   
    appliedTax : List[CustomerBillItemTax] = Field(description="Taxes associated with the Bill Item.")
    appliedFee : List[CustomerBillItemFee] = Field(description="Fees associated with the Bill Item.")
    customerBillItemType : MEFPriceType
    description : str = Field(default="", description="A text description of the charge.")
    periodCoverage : TimePeriod
    product : ProductRef
    productOrderItem : MEFProductOrderItemRef
    productName : str = Field(description="The name of the Product that is the subject of the Bill Item.", min_length=1)  
    state : CustomerBillItemStateType
    taxExcludedAmount : Money
    unit : str = Field(description="The rate per unit for the Bill determined during or after the Billing Process.")
    unitRate : Money
    unitQuantity : int = Field(description="The number of units.")
    
class CustomerBillEventType(str, Enum):
    
    """
    Type of the Bill Event
    """
    CUSTOMERBILLCREATEEVENT = "customerBillCreateEvent"
    CUSTOMERBILLSTATECHANGEEVENT = "customerBillStateChangeEvent"

class CustomerBillEventPayload(BaseModel):
    """
    The identifier of the Bill being subject of this event.
    """
    sellerId : Optional[str] = Field(default="", description="The unique identifier of the organization that is acting as the Seller. MUST be specified in the request only when the requester entity represents more than one Seller.")
    id : str = Field(description='ID of the Bill attributed by quoting system', min_length=1)        
    href : Optional[str] = Field(default="", description='Hyperlink to access the Bill')
    buyerId : Optional[str] = Field (default="", description="The unique identifier of the organization that is acting as the a Buyer. MUST be specified in the request only when the responding represents more than one Buyer.")
        
class CustomerBillEvent(Event):
    '''
    Event class is used to describe the information structure used for notification.
    '''
    eventType : CustomerBillEventType 
    event : CustomerBillEventPayload    
