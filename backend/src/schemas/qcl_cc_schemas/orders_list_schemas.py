from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderHistoryLink(BaseModel):
    rel: Optional[str] = Field(
        default = "", 
        description="""
        Reference to the page link.

        Page reference - Description
        prev - indicates the previous page
        self - indicates the current page (self-reference)
        next - indicates the next page"""
        )
    href: Optional[str] = Field(
        default = "", 
        description="The link to the page that is before, current, or next."
        )


class AccountInformation(BaseModel):
    accountName: Optional[str] = Field(
        default = "", 
        description="Cage account name linked to the customer."
        )
    accountNumber: Optional[str] = Field(
        default = "", 
        description="Cage account number linked to the customer."
        )
    
class MetaData(BaseModel):
    pricingEnforcementFlag: Optional[str] = Field(
        default = "", 
        description="""
        This is an Equinix reference. 

        You may ignore this.
        """
        )
    
class OrderingContactInformation(BaseModel):
    firstName: Optional[str] = Field(
        default = "", 
        description="First name of the Ordering contact."
    )
    lastName: Optional[str] = Field(
        default = "", 
        description="Last name of the Ordering contact."
    )
    workPhone: Optional[str] = Field(
        default = "", 
        description="Work phone number of the Ordering contact."
    )
    contactUCId: Optional[str] = Field(
        default = "", 
        description="""
        Equinix reference of the Ordering contact. 

        You may ignore this.
        """
    )
    username: Optional[str] = Field(
        default = "", 
        description="Equinix-registered username of the Ordering contact."
    )
    emailAddress: Optional[str] = Field(
        default = "", 
        description="Email address of the Ordering contact person."
    )

class NotificationContactInformation(BaseModel):
    phone: Optional[str] = Field(
        default = "", 
        description="Mobile phone number of the Notification contact."
    )
    workPhone: Optional[str] = Field(
        default = "", 
        description="Work phone number of the Notification contact."
    )
    lastName: Optional[str] = Field(
        default = "", 
        description="Last name of the Notification contact."
    )
    firstName: Optional[str] = Field(
        default = "", 
        description="First name of the Notification contact."
    )
    contactUCId: Optional[str] = Field(
        default = "", 
        description="""
        Equinix reference of the Notificaiton contact. 

        You may ignore this."""
    )
    emailAddress: Optional[str] = Field(
        default = "", 
        description="Email address of the Notification contact person."
    )
    username: Optional[str] = Field(
        default = "", 
        description="Equinix-registered username of the Notification contact person."
    )

class TechnicalContactInformation(BaseModel):
    firstName: Optional[str] = Field(
        default = "", 
        description="First name of the Technical contact."
    )
    lastName: Optional[str] = Field(
        default = "", 
        description="Last name of the Technical contact."
    )
    workPhone: Optional[str] = Field(
        default = "", 
        description="Work phone number of the Technical contact."
    )
    contactUCId: Optional[str] = Field(
        default = "", 
        description="""
        Equinix reference of the Technical contact. 

        You may ignore this.
        """
    )
    username: Optional[str] = Field(
        default = "", 
        description="Equinix-registered username of the Technical contact person."
    )
    email: Optional[str] = Field(
        default = "", 
        description="Email address of the Technical contact person."
    )

class EQXOrderDetailsList(BaseModel):
    orderNumber: Optional[str] = Field(
        default = "", 
        description="The order number."
        )
    createdAt: Optional[datetime] = Field(
        default=None,
        description="""
        The date and time the order was created.

        This follows the date and time (UTC timezone) in the ISO 8601 format."""
        )
    orderStatus: Optional[str] = Field(
        default = "", 
        description="""
        The current status of the order.

        Refer to description of body parameter "orderStatus"."""
        )
    orderSource: Optional[str] = Field(
        default = "", 
        description="""
        The source where the order was created. 

        Order source types - Description
        Portal - Order came via the customer portal.
        Offline - Order came via offline methods.
        Quote - Order came via quotation. 
        Mobile - Order came via Equinix Mobile."""
        )
    account: Optional[AccountInformation] = Field(
        default = None,
        description="""Account information that includes account name and account number."""
        )
    uiMetaData: Optional[MetaData] = Field(
        default = None,
        description="""
        This is an Equinix reference. 

        You may ignore this."""
        )
    orderingContacts: Optional[OrderingContactInformation] = Field(
        default = None,
        description="Contact information of the Ordering contact person that includes their\
        first name, last name, work phone number, username, and email address."
        )
    notificationContacts: Optional[List[NotificationContactInformation]] = Field(
        default = None,
        description="Contact information of the Notification contact person(s)\
        that includes their phone number, work phone number, first name,\
        last name, work phone number, username, and email address."
        )
    ibx: Optional[List[str]] = Field(
        default = [],
        description="""
        IBX location code(s) of the IBX data center linked to this order.

        E.g. PAA represents an IBX in Paris, France.
        """
    )
    type: Optional[List[str]] = Field(
        default = [],
        description="""
        The product types linked to this order. There may be more than one product type in an order.

        Refer to description of body parameter "productTypes".
        """
    )
    customerReferenceNumber: Optional[str] = Field(
        default = "", 
        description="Customer reference number that was provided by the \
            customer when the order was created."
        )
    poNumbers: Optional[List[str]] = Field(
        default = [],
        description="Purchase order numbers that are linked to this order. \
        There may be more than one purchase order number linked to an order."
    )
    piiHoldFlag: Optional[bool] = Field(
        default = False,
        description="""
        Indicates if this order was flagged for a PII hold.

        If 'true', the order will be held and will not proceed.

        If 'false', the order will not be held and will proceed.
        """
    )
    technicalContacts: Optional[List[TechnicalContactInformation]] = Field(
        default = None,
        description="Contact information of the Technical contact person that includes their phone number, \
            work phone number, first name, last name, work phone number, username, and email address."
    )
    pendingCustomerInputFlag: Optional[bool] = Field(
        default = False,
        description="""
        Indicates if this order was flagged for additional customer input.

        If 'true', the order will be held until the customer provides the required information.

        If 'false', the order will not be held and will proceed.
        """
    )
    awaitingCustomerResponse: Optional[bool] = Field(
        default = False,
        description="""
        Indicates if this order is pending customer response.

        If 'true', the order will be held until the customer responds.
        If 'false', the order will not be held and will proceed.
        """
    )
    srNumber: Optional[str] = Field(
        default = "", 
        description="The Equinix service request number linked to the order."
        )
    cancellable: Optional[bool] = Field(
        default = False,
        description="""
        Indicates if the order can still be canceled.

        If 'true', order can be canceled.

        If 'false', order cannot be canceled.
        """
    )
    modifiable: Optional[bool] = Field(
        default = False,
        description="""
        Indicates if the order can still be modified.

        If 'true', order can be modified.

        If 'fasle', order cannot be modified.
        """
    )
    links: Optional[List[OrderHistoryLink]] = Field(
        default = None,
        description="Link to full details of the order."
        )

class PageInformation(BaseModel):
    size: Optional[int] = Field(
        ge=1,
        le=200,
        default = 1,
        description="""
        Size of the information displayed per page.

        In this case, it is the number of orders displayed per page, and this tallies with body parameter 'size' in the submitted request.

        The minimum value is 1 and the maximum value is 200.
        """
    )
    totalElements: Optional[int] = Field(
        default = None,
        description="Total elements or total number of orders for the requested order history."
    )
    totalPages: Optional[int] = Field(
        default = None,
        description="""
        Total number of full pages for the requested order history, including the starting page '0'.

        I.e. If total elements divided by the size gives you a whole number, the total pages includes the final page.
            E.g. If size is 1 and totalElements is 19, totalPages is 19 (there are a total of 19 pages ranging from 0-18).

        I.e. If total elements divided by the size gives you a fraction/ decimal, the total pages does not include the final page.
            E.g. If size is 2 and totalElements is 19, totalPages is 9 (but there are a total of 10 pages ranging from 0-9).
        """
    )
    number: Optional[int] = Field(
        default = None,
        description="""
        The page number index of the order history to be returned. 

        This tallies with body parameter 'number' in the submitted request. The starting number is 0, and it represents the first page.
        """
    )


class OrdersEQXListResponse(BaseModel):
    links: Optional[List[OrderHistoryLink]] = Field(
        default = None,
        description="""
        Hateoas information with self, previous and next links.
                    
        These display the previous, current, or next pages for the order history."""
        )
    
    content: Optional[List[EQXOrderDetailsList]] = Field(
        default = None,
        description="Order content contains the order objects."
        )
    
    page: Optional[PageInformation] = Field(
        default = None,
        description="Page information that includes the requested size of the information \
            displayed, the total number of elements in the order history, the total number of \
            pages in the order history, and the page index number."
        )
    


# CYX

class Type(BaseModel):
    id: Optional[int] = Field(
        default = None,
    )
    name: Optional[str] = Field(
        default = ""
    )

class AccountDetails(BaseModel):
    alias: Optional[str] = Field(
        default = ""
    )
    type: Optional[Type] = Field(
        default = None
    )
    status: Optional[Type] = Field(
        default = None
    )
    bpId: Optional[str] = Field(
        default = ""
    )
    ban: Optional[str] = Field(
        default = ""
    )
    sfdc: Optional[str] = Field(
        default = ""
    )
    wcoApproved: Optional[bool] = Field(
        default = False
    )
    partner: Optional[str] = Field(
        default = ""
    )
    id: Optional[str] = Field(
        default = ""
    )
    name: Optional[str] = Field(
        default = ""
    )

class DataCenterObject(BaseModel):
    id: Optional[str] = Field(
        default = ""
    )
    name: Optional[str] = Field(
        default = ""
    )

class CYXOrderDetailsList(BaseModel):
    account: Optional[AccountDetails] = Field(
        default = None
    )
    id: Optional[str] = Field(
        default = ""
    )
    number: Optional[str] = Field(
        default = ""
    )
    state: Optional[Type] = Field(
        default = None
    )
    dataCenter: Optional[DataCenterObject] = Field(
        default = None
    )
    shortDescription: Optional[str] = Field(
        default = ""
    )
    openedAt: Optional[datetime] = Field(
        default = None,
        description="Enables basic storage and retrieval of dates and times."
    )
    createdAt:  Optional[datetime] = Field(
        default = None,
        description="Enables basic storage and retrieval of dates and times."
    )
    quote: Optional[str] = Field(
        default = ""
    )

class OrdersCYXListResponse(BaseModel):
    items: Optional[List[CYXOrderDetailsList]] = Field(
        default = None
    )
    type: Optional[str] = Field(
        default = ""
    )
    totalRecordCount: Optional[int] = Field(
        default = None,
    )
    pageNumber: Optional[int] = Field(
        default = None,
    )
    pageSize: Optional[int] = Field(
        default = None,
    )

from typing import Dict

from .cross_connect_move_schemas import QclGenericDataObject
from .cross_connect_order_schema import DestinationFields, GenericFields


class QCLOrdersTransactionData(BaseModel):
    genericFields: GenericFields = Field(default={})
    sourceFields: Dict = Field(default={})
    destinationFields: DestinationFields = Field(default={})

class OrdersListObject(BaseModel):
    genericData: QclGenericDataObject
    transactionData: QCLOrdersTransactionData
