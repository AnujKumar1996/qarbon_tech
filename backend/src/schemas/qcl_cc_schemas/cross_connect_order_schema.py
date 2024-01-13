from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class QclTypeEnum(str, Enum):
    PHONE = "PHONE"
    MOBILE = "MOBILE"
    EMAIL = "EMAIL"
    
class QclpeConnectorTypeEnum(str, Enum):
    BNC = "BNC"
    LC = "LC"
    FC = "FC"
    SC = "SC"
    ST = "ST"
    WIRE_WRAP = "WIRE_WRAP"
    RJ45 =  "RJ45"
    E2000 = "E2000"
    RJ11 = "RJ11"


class QclCrossconnectNotificationDetails(BaseModel):
    type : Optional[QclTypeEnum] = Field(default=None)
    value : Optional[str] = Field(default=None)

class QclCrossconnectContacts(BaseModel):
    southUsername : Optional[List[str]] = Field(default=None)
    availability : Optional[str] = Field(default=None) 
    timezone : Optional[str] = Field(default=None)
    contactType : Optional[str] = Field(default=None)
    firstName : Optional[str] = Field(default=None)
    lastName : Optional[str] = Field(default=None)
    notificationDetails : Optional[List[QclCrossconnectNotificationDetails]] = Field(default=None)
    
class QclCrossconnectccPatchEquipmentDetails(BaseModel):
    peCabinetId : Optional[str] = Field(default=None)
    peConnectorType : Optional[QclpeConnectorTypeEnum] = Field(default=None)
    peAdditionalDetails : Optional[str] = Field(default=None)
    pePort : Optional[int] = Field(default=None)

class QclCrossconnectattachmentDetails(BaseModel):
    ccattachmentId : Optional[str] = Field(default=None)
    attachmentName : Optional[str] = Field(default=None)
    
class QclCrossconnectpurchaseOrderDetails(BaseModel):
    poType  : Optional[str] = Field(default=None)
    poNumber : Optional[str] = Field(default=None)
    poAmount : Optional[str] = Field(default=None)
    poStartDate : Optional[str] = Field(default=None)
    poEndDate : Optional[str] = Field(default=None) 
    ccattachmentId : Optional[str] = Field(default=None)


class QclItemDeinstallDetail(BaseModel):
    ccDeinstallId: str
    ccRemovalDate: date
    customerReferenceId : Optional[str] = Field(default=None)
    description : Optional[str] = Field(default=None)
    ccPatchEquipmentDetails : Optional[QclCrossconnectccPatchEquipmentDetails] = Field(default=None)
    attachmentDetails : Optional[List[QclCrossconnectattachmentDetails]] = Field(default=None)
    purchaseOrderDetails : Optional[QclCrossconnectpurchaseOrderDetails] = Field(default=None)
    proceedWithLiveTraffic : Optional[bool] = Field(default=False)
    contacts :  Optional[List[QclCrossconnectContacts]] = Field(default=None)
 
     
class QclCrossconnectCYXZSideDetails(BaseModel):
    ccZSideProviderName: Optional[str] = Field(default=None)
    ccIbx : Optional[str] = Field(default=None)
    ccLoaAttachmentId : Optional[str] = Field(default=None)

class ConnectionType(str, Enum):
    BNC = "BNC"
    LC = "LC"
    FC = "FC"
    SC = "SC"
    ST = "ST"
    WIRE_WRAP = "WIRE_WRAP"
    RJ45 = "RJ45"
    E2000 = "E2000"
    RJ11 = "RJ11"
    
class QclCrossconnectEQXZSideDetails(QclCrossconnectCYXZSideDetails):
    ccConnectorType: Optional[ConnectionType] = Field(default=None)
    ccZSidePatchPanelId: Optional[str] = Field(default=None)
    ccPatchPanelPortA: int = Field(default=None)
    ccPatchPanelPortB: int = Field(default=None)
    ccCircuitId : str = Field(default=None)
    notificationEmail : str = Field(default=None)

class QclCrossconnectZSideDetails(QclCrossconnectEQXZSideDetails):
    pass

class QclCrossconnectCYXASideDetails(BaseModel):
    ccAccountId: str = Field(default=None)
    ccPodId: str = Field(default=None)
    ccModelId: str = Field(default=None)
    ccPortId: str = Field(default=None)

class ConnectionServiceType(str, Enum):
    COAX = 'COAX'
    MP4_CABLE = "MP4_CABLE"
    MULTI_MODE_FIBER = "MULTI_MODE_FIBER"
    POTS = "POTS"
    SINGLE_MODE_FIBER = "SINGLE_MODE_FIBER"
    UTP = "UTP"

class MediaType(str, Enum):
    COAX = 'COAX'
    MP4_CABLE = "MP4_CABLE"
    MICRON_MULTI_MODE_FIBER = "50_MICRON_MULTI_MODE_FIBER"
    MICRON_MULTI_MODE_FIBER_OM2 = "50_MICRON_MULTI_MODE_FIBER_OM2"
    MICRON_MULTI_MODE_FIBER_OM3 = "50_MICRON_MULTI_MODE_FIBER_OM3"
    MICRON_MULTI_MODE_FIBER_OM4 = "50_MICRON_MULTI_MODE_FIBER_OM4"
    MICRON_MULTI_MODE_FIBER_62_5 = "62.5_MICRON_MULTI_MODE_FIBER"
    MICRON_MULTI_MODE_FIBER_OM1_62_5 = "62.5_MICRON_MULTI_MODE_FIBER_OM1"
    ABAM = "ABAM"
    CAT3 = "CAT3"
    CAT5E = "CAT5E"
    CAT6 = "CAT6"
    CAT6A = "CAT6A"
    OS1 = "OS1"
    SINGLE_MODE_FIBER = "SINGLE_MODE_FIBER"

class ProtocolType(str, Enum):
    K = "56K"
    ANTENNA = "ANTENNA"
    DS = "DS-3"
    E1 = "E1"
    E3 = "E3"
    ETHERNET = "ETHERNET"
    FAST_ETHERNET = "FAST_ETHERNET"
    GIGABIT_ETHERNET = "GIGABIT_ETHERNET"
    POTS = "POTS"
    T1 = "T1"
    FIBRE_CHANNEL = "FIBRE_CHANNEL"
    GIG_ETHERNET_10 = "10_GIG_ETHERNET"
    GIG_ETHERNET_100 = "100_GIG_ETHERNET"
    GIG_ETHERNET_40 = "40_GIG_ETHERNET"
    DARK_FIBER = "DARK_FIBER"
    DWDM = "DWDM"
    ISDN = "ISDN"
    OC12 = "OC-12"
    OC192 = "OC-192"
    OC3 = "OC-3"
    OC48 = "OC-48"
    STM1 = "STM-1"
    STM16 = "STM-16"
    STM4 = "STM-4"
    STM64 = "STM-64"
    NA = "NA"
    
class QclCrossconnectdcPatchPanelDetails(BaseModel):
    dcPatchPanelId : Optional[str] = Field(default=None)
    dcPatchPanelPortA : Optional[int] = Field(default=None)
    dcPatchPanelPortB : Optional[int] = Field(default=None)
    
class QclCrossconnectdcPatchEquipment(BaseModel):
    peAdditionalDetails : Optional[str] = Field(default=None)
    peCabinetId : Optional[str] = Field(default=None)
    peConnectorType : Optional[str] = Field(default=None)
    peDetails : Optional[str] = Field(default=None)
    pePort : Optional[int] = Field(default=None)
    

class QclCrossconnectdcASideDetails(BaseModel):
    dcPatchPanelDetails : Optional[QclCrossconnectdcPatchPanelDetails] = Field(default=None)
    dcConnectorType : Optional[str] = Field(default=None)
    dcMediaConverterRequired : Optional[bool] = Field(default=False)
    dcIfcCircuitCount : Optional[int] = Field(default=None)
    dcPatchEquipment : Optional[QclCrossconnectdcPatchEquipment] = Field(default=None)
    
class QclCrossconnectdcZSideDetails(BaseModel):
    dcPatchPanelDetails : Optional[QclCrossconnectdcPatchPanelDetails] = Field(default=None)
    dcConnectorType : Optional[str] = Field(default=None)
    dcIfcCircuitId : Optional[str] = Field(default=None)
    
class QclCrossconnectDiverseConnectionDetails(BaseModel):
    dcType : Optional[str] = Field(default=None)
    dcSerialNumber : Optional[str] = Field(default=None)
    dcASideDetails : Optional[QclCrossconnectdcASideDetails] = Field(default=None)
    dcZSideDetails : Optional[QclCrossconnectdcZSideDetails] = Field(default=None)

class QclCrossconnectEQXASideDetails(QclCrossconnectCYXASideDetails):
    ccConnectionService: Optional[ConnectionServiceType] = Field(None)
    ccMediaType: Optional[MediaType] = Field(None) #added as per QCL schema.
    ccProtocolType: Optional[ProtocolType] = Field(None)
    ccConnectorType: Optional[ConnectionType] = Field(None)
    ccASidePatchPanelId: str = Field(default=None)
    ccPatchPanelPortA: Optional[int] = Field(default=None)
    ccPatchPanelPortB: Optional[int] = Field(default=None)
    ccIfcCircuitCount : Optional[int] = Field(default=None)
    ccMediaConverterRequired : Optional[bool] = Field(default=False)
    ccPatchEquipmentDetails : Optional[QclCrossconnectccPatchEquipmentDetails] = Field(default=None)
    

class QclCrossconnectASideDetails(QclCrossconnectEQXASideDetails):
    pass

class QclCrossconnectDetails(BaseModel):
    ccRequestDate: Optional[date] = Field(default=None) #Added as per QCL schema.
    ccExpediteTime : Optional[str] = Field(default=None,description="Expedite orders are delivered within the next 2 - 24 hours. Value must be in ISO-8601 UTC timezone format.")
    description  : Optional[str] = Field(default=None,description="Additional description for order crossconnect")
    customerReferenceId : Optional[str] = Field(default=None)
    ccASideDetails: QclCrossconnectASideDetails
    ccZSideDetails: QclCrossconnectZSideDetails
    ccDiverseConnectionDetails : Optional[QclCrossconnectDiverseConnectionDetails] = Field(default=None)
    ccVerifyLink : Optional[bool] = Field(default=False)
    ccCircuitDeliveryDate : Optional[str] = Field(default=None)
    ccSubmarineEngineerRequired : Optional[bool] = Field(default=False)
    attachmentDetails : Optional[List[QclCrossconnectattachmentDetails]] = Field(default=None)
    purchaseOrderDetails : Optional[QclCrossconnectpurchaseOrderDetails] = Field(default=None)
    proceedWithLiveTraffic : Optional[bool] = Field(default=False)
    contacts :  Optional[List[QclCrossconnectContacts]] = Field(default=None)


class QclItemDetails(BaseModel):
    inventoryItemName: str
    crossConnectDetails: Optional[QclCrossconnectDetails] = Field(default=None)
    originalItemDetails: list[str] = Field(default=[]) #list[str] as per QCL schema docs.
    ccDeinstallDetails: Optional[QclItemDeinstallDetail] = Field(default=None)

class SourceOrderFields(BaseModel):
    iaId: Optional[str] = Field(default=None)
    itemDetails: List[QclItemDetails]

class SourceFields(SourceOrderFields):
    pass

class GenericFields(BaseModel):
    pass

class DestinationFields(BaseModel):
    pass

class QclTransactionDataObject(BaseModel):
    genericFields: GenericFields = Field(default={})
    sourceFields: SourceFields
    destinationFields: DestinationFields = Field(default={})

class QclObject(BaseModel):
    transactionData: QclTransactionDataObject
