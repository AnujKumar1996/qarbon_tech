from typing import List
from pydantic import BaseModel, Field


class OriginalItemDetails(BaseModel):
    ccCancelReason : str = Field(min_length = 5)

class QclItemDetails(BaseModel):
    inventoryItemId   : str = Field(min_length = 1)
    inventoryItemName : str = "Cross Connect"
    inventoryItemId   : str
    #ccCancelDetails   : OriginalItemDetails #= Field(default={}) #dict or list[str] as per QCL schema docs.
    originalItemDetails : list[str] = Field(default=[])

class SourceFields(BaseModel):
    #iaId : str
    itemDetails: List[QclItemDetails]
    

class GenericFields(BaseModel):
    pass

class DestinationFields(BaseModel):
    pass

class QclTransactionDataObject(BaseModel):
    genericFields: GenericFields = Field(default={})
    sourceFields: SourceFields
    destinationFields: DestinationFields = Field(default={})

class QclObject(BaseModel):
    # qcl_generic_data: QclGenericDataObject
    transactionData: QclTransactionDataObject
