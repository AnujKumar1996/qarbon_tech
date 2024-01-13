from pydantic import BaseModel, Field
from src.schemas.qcl_cc_schemas.cross_connect_order_schema import (
    DestinationFields, GenericFields)
from src.schemas.qcl_cc_schemas.cross_connect_move_schemas import (
    NorthEntity, SouthEntity)

class SourceOrderFields(BaseModel):
    orderId: str

class SourceFields(SourceOrderFields):
    pass


class QclTransactionDataObject(BaseModel):
    genericFields: GenericFields = Field(default={}) # Required as per qcl schema
    sourceFields: SourceFields
    destinationFields: DestinationFields = Field(default={}) 

class QclGenericDataObject(BaseModel):
    sourceId: NorthEntity
    destinationId: SouthEntity

class QclOrderDetails(BaseModel):
    genericData: QclGenericDataObject
    transactionData: QclTransactionDataObject