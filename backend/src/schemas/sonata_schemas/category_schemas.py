from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class CategoryRef(BaseModel):
    id: str = Field(
        description="Unique identifier (within the Seller domain) for the Product Category."
        )
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to access the Category"
        )

class ProductOfferingRef(BaseModel):
    id: str = Field(
        description="Unique (within the Seller domain) identifier for the Product Offering."
        )
    href: Optional[str] = Field(
        default="",
        description="Hyperlink to access the Product Offering"
        )

class CategoryLifecycleStatusType(str, Enum):
    """
    | Name                       | MEF 127 Name     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
    | -------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | active                     | AVAILABLE        | A Product Category is in the `active` state when it can be used by the Buyer to retrieve Product Offerings and Product Specifications.                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | obsolete                   | OBSOLETE         | A Product Category is `obsolete` when it can no longer be used by the Buyer to retrieve Product Offerings or Product Specifications. The Product Category may be removed from the Product Catalog. This is a final state.                                                                                                                                                                                                                                                                                                                                                           |
    """
    ACTIVE     = 'active'
    OBSOLETE = 'obsolete'

class ProductCategory(CategoryRef):
    name: str = Field(
        description="The name (unique within the Seller domain) of the Product Category"
        )
    description: str = Field(
        description="Description of the Product Category"
        )
    lastUpdate: datetime = Field(
        description="The date and time the Product Category was created or most recently updated."
        )
    lifecycleStatus:CategoryLifecycleStatusType
    parentCategory: Optional[CategoryRef] = Field(
        default=None,
        description="A list of references to Product Category, to which this Product Category is a parent of."
    )
    subCategory: Optional[List[CategoryRef]] = Field(
        default=None,
        description="A list of references to Product Category, to which this Product Category is a parent of."
    )
    productOffering: Optional[List[ProductOfferingRef]] = Field(
         default=None,
        description="A list of references to Product Offering grouped within this Category."
    )