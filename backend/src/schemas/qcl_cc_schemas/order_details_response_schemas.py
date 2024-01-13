from pydantic import BaseModel,Field
from typing import List, Optional

class Details(BaseModel):
    type : Optional[str] = Field(default="",description='''Type of contact detail in the type-value pair. Type - Description
                                    PHONE - Primary phone number. 
                                    EMAIL - Email address.
                                    MOBILE - Mobile phone number. This is the secondary contact number.''')
    value : Optional[str] = Field(default="",description="Value related to the contact detail type in the type-value pair.")
    

class Contacts(BaseModel):
    firstName : Optional[str] = Field(default="",description="First name of contact person.")
    lastName  : Optional[str] = Field(default="",description="Last name of contact person.")
    registeredUser : Optional[str] = Field(default="",description="Equinix Customer Portal username of the registered contact. This is only applicable for contacts who are registered users of the Equinix Customer Portal.")
    availability : Optional[str] = Field(default="",description="Availability of the contact to receive calls from Equinix.")
    timezone : Optional[str] = Field(default="",description="Contact's timezone.")
    details : Optional[List[Details]] = Field(default=None,description="List of contact details for this person.Each contact detail object consists of the following fields: type, value.")
    type    : Optional[str] = Field(default="",description='''Type of communication contact.
                                    Type - Description
                                    ORDERING - Ordering contact is the user who submitted this order. 
                                    NOTIFICATION - Notification contact is the person who will be notified of status updates for this order.
                                    TECHNICAL - Technical contact is the person who Equinix can reach for technical clarifications
                                    RESELLER - Reseller is the contact person in an organization who made the order on behalf of their customer.''')
                                        
class AdditionalInfo(BaseModel):
    key : Optional[str] = Field(default="",description="Name of the key in the key-value pair. For more information on the additional details that can be associted with an order, see")
    value : Optional[str] = Field(default="",description="Value related to the key in the information key-value pair.")
    customerReferenceId : Optional[str] = Field(default="",description="Customer's reference ID for this order. This was provided by customer during order submission.")
    cancellable : bool = Field(default=False,description="Indicates if the order can still be cancelled. If true, the order can be cancelled. If false, otherwise.")
    modifiable : bool = Field(default=False,description="Indicates if the order can still be modified. If true, the order can be modified. If false, otherwise.")
    
    
class UnitPricing(BaseModel):
    value : Optional[float] = Field(default=None,description="Numerical value of the unit cost of this order line. The pricing terms of this value is defined by the valueType.")
    valueType : Optional[str] = Field(default="",description='''Defines the terms of pricing associated with the value.
                                    Value type - Description
                                    ABSOLUTE - Value is an absolute value in the monetary unit defined by the parameter 'currencyCode'.
                                    PERCENTAGE - Value is a percentage.''')
    type : Optional[str] = Field(default="",description='''Type of charge.
                            Type - Description
                            ONE_TIME_CHARGE - An ad-hoc charge.
                            MONTHLY_CHARGE - A monthly, recurring charge.
                            MONTHLY_DISCOUNT - A discount that is applied on a recurring, monthly basis. 
                            ONE_TIME_DISCOUNT - A discount that is applied once.''')
    
    
class TotalPricing(BaseModel):
    value : Optional[float] = Field(default=None,description="Numerical value of the total cost of this order line. The pricing terms of this value is defined by the valueType.")
    valueType : Optional[str] = Field(default="",description='''Defines the terms of pricing associated with the value.
                            Value type - Description
                            ABSOLUTE - Value is an absolute value in the monetary unit defined by the parameter 'currencyCode'.
                            PERCENTAGE - Value is a percentage.''')
    type : Optional[str] = Field(default="",description='''Type of charge.
                            Type - Description
                            ONE_TIME_CHARGE 
                            MONTHLY_CHARGE
                            MONTHLY_DISCOUNT
                            ONE_TIME_DISCOUNT''')
    
class AdditionalInfoDetails(BaseModel):
    key : Optional[str] = Field(default="",description="Name of the detail in the key-value pair.")
    value : Optional[str] = Field(default="",description="Value of associated detail in the key-value pair. In case of external ID (for example S/No.1001.1.1) this is customer's reference ID specific to the order line. This appears when an external ID is mapped to this order line.")
    
class PurchaseOrder(BaseModel):
    type   : Optional[str] = Field(default="",description='''Type of purchase order associated with this order line.
                            Type - Description
                            EXEMPTED - Account is exempted from including purchase order information.
                            NEW - New purchase order that has not yet been used.  
                            EXISTING - Purchase order that is already in use.''')
    number : Optional[str] = Field(default="",description="Purchase order reference number.")
    closingDate : Optional[str] = Field(default="",description="Expiration of the purchase order.")
    
    
class Attachments(BaseModel):
    id   : Optional[str] = Field(default="",description="Attachment ID.")
    name : Optional[str] = Field(default="",description="Name of attachment.")
    
    
class DetailsObj(BaseModel):
    lineId : Optional[str] = Field(default="",description="ID of the order line. Each order line ID is unique.")
    parentLineId : Optional[str] = Field(default="",description='''ID of the parent order line for lineId, if this order line is part of a hierarchy that is more than two levels.
                                    This is null when the order line is at the root line level.''')
    rootLineId  : Optional[str] = Field(default="",description='''ID of the root order line. This is the first level (root) order line.
                                  For example, rootLineId1-2J3PJA4E is the first-level order line, parentLineId 1-2J3PJA23 stems from this first-level order line, and lineId 1-2J3PJADP directly stems from parentLineId .''')
    status : Optional[str] = Field(default="",description="Current status of the order line.")
    expediteDateTime : Optional[str] = Field(default="",description="Expedited date and time (UTC timezone) that customer expects this order to be completed. This appears when a customer requires the order to be completed within 2 to 24 hours from the time the order was created.")
    description : Optional[str] = Field(default="",description="Description of the order line. ")
    billingStartDateTime : Optional[str] = Field(default="",description="Date and time that Equinix billing has started for this order line. Billing is triggered when the order line is completed or closed.")
    unitPricing : Optional[List[UnitPricing]] = Field(default=None,description="Price per unit of this order line. Each unit price object comprises the following fields: value, valueType, type.")
    totalPricing : Optional[List[TotalPricing]] = Field(default=None,description="Total price of this order line. Each total price object comprises the following fields: value, valueType, type.")
    productType : Optional[str] = Field(default="",description='''Type of product ordered.
                                Product type - Description
                                CROSS_CONNECT - Orders for installing cross connections. 
                                SMART_HANDS - Orders for Smart Hands requests.
                                WORK_VISIT - Orders for scheduled work visits including registered and non-registered visitors.
                                SECURITY_ACCESS - Orders for granting or removing security access.
                                CONFERENCE_ROOM - Orders for conference room reservations.
                                TROUBLE_TICKET - Orders for trouble tickets.
                                SHIPMENTS - Orders for inbound or outbound shipments. 
                                NETWORK_PORTS - Orders for network ports.
                                DEINSTALL_CROSS_CONNECT - Orders for removing cross connections. 
                                OTHER - All other order types.''')
    productCode : Optional[str] = Field(default="",description="Product code paired with 'productName' associated with this order line.")
    productName : Optional[str] = Field(default="",description='''Product name paired with the 'productCode' associated with this order line. 
                                    If you are placing work visit orders, the product name displays as:
                                    •“Contact” for registered user
                                    •“Visitor” for non-registered visitor
                                    Refer to the work visit of the 'productType''')
    ibx  : Optional[str] = Field(default="",description="IBX code associated with this order line.")
    cage : Optional[str] = Field(default="",description="Cage ID associated with this order line.")
    cabinets : Optional[str] = Field(default="",description="List of cabinet IDs associated with this order line, if applicable.")
    requestType : Optional[str] = Field(default="",description='''Type of request action associated with this order line.
                                Request type - Description
                                ADD - A new product or part is added. For example, a device or part was upgraded.
                                DELETE - A product or part was removed or deleted. 
                                NO_CHANGE -  There is no change to the product or part.
                                UPDATE - A product or part was updated.''')
    additionalInfo : Optional[List[AdditionalInfoDetails]] = Field(default=None,description='''Additional information associated with this order line.
                                            Each additional detail object comprises the following fields: key, value. 
                                            For more information about additional info for product type orders, see Orders: Managing Additional Info in the Appendix.''') 
    purchaseOrder : Optional[PurchaseOrder] = Field(default="",description='''Purchase order information associated with this order line. 
                                    Purchase order object comprises the following fields: type, number, closingDate.''') 
    attachments : Optional[List[Attachments]] = Field(default=None,description="Attachments array comprising object(s) with attachment details. Each attachment object contain the following parameters: id, name. ")
    

class Notes(BaseModel):
    id      :  Optional[str] = Field(default="",description="ID of the specific note.")
    referenceId : Optional[str] = Field(default="",description="Reference ID related to order activity.")
    createdDateTime : Optional[str] = Field(default="",description="Date and time the note was created.")
    text : Optional[str] = Field(default="",description="Text in the note. ")
    author : Optional[str] = Field(default="",description="Author of the note. For example, EQIX_SUPPORT represents the Equinix technician who authored the note.")
    type : Optional[str] = Field(default="",description='''Type of note.
                            Type - Description
                            CUSTOMER_QUERY - Customer reply to Equinix technician query.
                            CUSTOMER_NOTES - Notes provided by the customer in text or attachment form. 
                            TECHNICIAN_QUERY - Query from the Equinix technician to the customer. Customer query should be sent to response to this Technician query.''')
    attachments : Optional[List[Attachments]] = Field(default=None,description="Attachments array comprising object(s) with attachment details. Each attachment object contain the following parameters: id, name. ")
                                          
class EYX_Order_details(BaseModel): 
    orderId : Optional[str] = Field(default="",description="Order ID, also known as the order number in the Equinix Customer Portal.")
    accountName : Optional[str] = Field(default="",description="Customer account name associated with the order.")
    accountNumber : Optional[str] = Field(default="",description="Customer account number associated with the order.")
    contacts  : Optional[List[Contacts]] = Field(default=None,description="Contacts array comprises objects representing the ordering, notification and technical contacts. Each object contains the following parameters where applicable: firstName, lastName, registeredUser, availability, timezone, details, type. Equinix communicates with these contacts based on the listed contact information.")
    status : Optional[str] = Field(default="",description=''''Current order status.
                                'Status - Description
                                RECEIVED - Ticket is entered, booked, or submitted in the system.
                                IN_PROGRESS - Order fulfillment is in progress, or order is in-between status change. 
                                ON_HOLD - Order is on hold. Further action may be required from Equinix or customer before order can be fulfilled.
                                CLOSED - Order is fulfilled and closed. 
                                CANCELLED - Order is cancelled.''')
    createdDateTime : Optional[str] = Field(default="",description="Date and time (UTC timezone) the order was created.ISO 8601 format: yyyy-MM-dd'T'HH:mm:ssZ.")
    updatedDateTime : Optional[str] = Field(default="",description="Latest date and time (UTC timezone) the order was updated. ISO 8601 format: yyyy-MM-dd'T'HH:mm:ssZ.") 
    closedDateTime : Optional[str] = Field(default="",description="Date and time (UTC timezone) order completed and closed. ISO 8601 format: yyyy-MM-dd'T'HH:mm:ssZ.")
    channel : Optional[str] = Field(default="",description='''Equinix ordering channel.
                                Channel- Description  
                                API - Order was submitted via API.
                                PORTAL - Order was submitted through an Equinix Portal Web based application.
                                MOBILE - Order was submitted through an Equinix Portal Mobile App. 
                                OFFLINE - Order was submitted to Global Service Desk or to your Customer Success Manager.''')
    subChannel : Optional[str] = Field(default="",description='''Specific Equinix ordering sub-channel. This is the specific service through which the order originated, if applicable.
                                For example, an order with channel 'PORTAL' and sub-chanel 'ECP' means the other came through the Equinix Customer Portal Web based application.
                                Sub-channel - Description
                                ECP - Equinix Customer Portal
                                ECX - Equinix Fabric
                                IX - Equinix Internet Exchange
                                NE - Network Edge
                                EMG - Equinix Messaging Gateway
                                QUOTE - Quotation''')
    currencyCode : Optional[str] = Field(default="",description="Billing currency. Format: ISO 4217 Currency Code For a full list of currency codes, see Currency Codes in the Appendix.")
    additionalInfo : Optional[List[AdditionalInfo]] = Field(default=None,description="List of any additional details or information related to this order line. Each information object comprises the following fields: key, value.") 
    details : Optional[List[DetailsObj]] = Field(default=None,description='''List of order line details specific to this order.
                                            Each order line object contains the following parameters where applicable: 
                                            lineId, parentLineId, rootLineId, status, expediteDateTime, description, billingStartDateTime, unitPricing, totalPricing, productType, productCode, productName, ibx, cage, cabinets, requestType, additionalInfo, attachments.''')
    notes : Optional[List[Notes]] = Field(default=None,description="Notes array comprises objects that represents all notes and queries from Equinix and the customer for this order. Each object contains the following parameters where applicable: id, createdDateTime, text, referenceId, author, type, attachments.")
    quoteRequestType : Optional[str] = Field(default="",description="Type of available quotes.")
    

class State(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class DataCenter(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class Account(BaseModel):
    id  : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    alias : Optional[str] = Field(default="")
    
    
class AssignedTo(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class Project(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
    
class Pod(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class OrderContact(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class SalesRep(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class Product(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class Entitlement(BaseModel):
    id : Optional[str] = Field(default="")
    name : Optional[str] = Field(default="")
    
class LineItems(BaseModel):
    number : Optional[str] = Field(default="")
    serviceId : Optional[str] = Field(default="")
    listUnitPrice : Optional[int] = Field(default=None)
    convertedUnitPrice : Optional[int] = Field(default=None)
    quantity : Optional[int] = Field(default=None)
    netTotal: Optional[int] = Field(default=None)
    chargeType: Optional[str] = Field(default="")
    contractStart: Optional[str] = Field(default="")
    dcCurrency: Optional[str] = Field(default="")
    convertedNetTotal: Optional[int] = Field(default=None)
    serviceDeltaTotal: Optional[int] = Field(default=None)
    convertedServiceDeltaTotal: Optional[int] = Field(default=None)
    autoRenewString: Optional[str] = Field(default="")
    billStartDate: Optional[str] = Field(default="")
    approval: Optional[str] = Field(default="")
    billingFrequency: Optional[str] = Field(default="")
    forecastDate: Optional[str] = Field(default="")
    listNRCPrice: Optional[int] = Field(default=None)
    cancellationReason: Optional[str] = Field(default="")
    quoteType: Optional[str] = Field(default="")
    term: Optional[str] = Field(default="")
    freeMonths: Optional[str] = Field(default="")
    createdAt : Optional[str] = Field(default="")
    createdBy : Optional[str] = Field(default="")
    product : Optional[Product] = Field(default=None)
    entitlement : Optional[Entitlement] = Field(default=None)
    
class Comments(BaseModel):
    pass

class Attachments(BaseModel):
    fieldName : Optional[str] = Field(default="")
    contentType : Optional[str] = Field(default="")
    attachmentId : Optional[str] = Field(default="")
    internal : bool = Field(default=False)

class CQX_Order_details(BaseModel):
    id : Optional[str] = Field(default="")
    number : Optional[str] = Field(default="")
    createdAt : Optional[str] = Field(default="")
    shortDescription : Optional[str] = Field(default="")
    quote : Optional[str] = Field(default="")
    escalated : bool = Field(default=False)
    quoteType : Optional[str] = Field(default="")
    dcCurrency : Optional[str] = Field(default="")
    recurringTotal : Optional[int] = Field(default=None)
    nonRecurringTotal : Optional[int] = Field(default=None)
    nonRecurringTotalUSD : Optional[int] = Field(default=None)
    notes : Optional[str] = Field(default="")
    createdBy : Optional[str] = Field(default="")
    updatedBy : Optional[str] = Field(default="")
    updatedOn : Optional[str] = Field(default="")
    state : Optional[State] = Field(default=None)
    dataCenter : Optional[DataCenter] = Field(default=None)
    account : Optional[Account] = Field(default=None)
    assignedTo : Optional[AssignedTo] = Field(default=None)
    project : Optional[Project] = Field(default=None)
    pod :  Optional[Pod] = Field(default=None)
    orderContact : Optional[OrderContact] = Field(default=None)
    salesRep : Optional[SalesRep] = Field(default=None)
    lineItems : Optional[List[LineItems]] = Field(default=None)
    comments : Optional[List[Comments]] = Field(default=None)
    attachments : Optional[List[Attachments]] = Field(default=None)