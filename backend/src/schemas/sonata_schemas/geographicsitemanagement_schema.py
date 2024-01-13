from pydantic import BaseModel, Field
from typing import List, Optional
from .common_schemas import RelatedContactInformation
from enum import Enum

class MEFSiteType(str,Enum):
    
   """
   This defines whether a Geographic Site is public or private. public means that the existence of this Geographic Site is public information. A meet-me-room in a hosted data center facility (where all interconnects between parties take place) is an example of a public Geographic Site. A shared facility in the basement of a multi-tenant business building where all interconnects between parties take place is another example of a public Geographic Site. private means that the existence of this Geographic Site is on a need-to-know basis. A wiring closet set up inside a customer facility just to connect two parties is an example of a private Geographic Site. For private sites, the Seller does not return any information regarding the existence of this Geographic Site unless it has been established that this Buyer is authorized to obtain this information.
   """  
   PUBLIC ='public'
   PRIVATE='private'
   
class GeographicAddressRefOrValue(BaseModel):
    
    """
    Defines a GeographicAddress link by reference or by value. The polymorphic attributes @type and @schemaLocation are related to the GeographicAddress entity and not the GeographicAddressRefOrValue class itself.
    """ 
    type: Optional[str] = Field(
        default="",
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
    
class GeographicSite(BaseModel):
    
    """
    A fixed physical location at which a Product can be installed. Its location can be described either with geographic point (Lat/Long information) or by association with an Address or Geographic Address Label. This association may include a Sub-address describing where within that Address or Geographic Address Label this particular Geographic Site is located.
    """
    relatedContactInformation:Optional[List[RelatedContactInformation]]  =Field(default=None,
                                                                                description="An entity or organization that is involved to the geographical site, such as the Site Contact or Site Alternate Contact. ")
    type: Optional[str] = Field(
        default="",
        alias="@type",
        example="FieldedAddress",
        description="This field is used as discriminator. The value is the name of one of the types that inherit from it using 'allOf', i.e. one of FieldedAddress, FormattedAddress, GeographicAddressLabel, MEFGeographicPoint. Moreover, it might discriminate for an additional related place as defined in '@schemaLocation'."
        )
    companyName : Optional[str] = Field(default="",
                                        description="The name of the company that is the administrative authority (e.g. controls access) for this Geographic Site. (For example, the building owner.)")
    name : Optional[str] = Field(default="",
                                 description="A user-friendly name for the place, such as [Paris Store], [London Store], [Main Home]")
    description : Optional[str] = Field(default="",
                                        description="A textual description of the Geographic Site.")
    
    id : str = Field(min_length=1, description="Identifier of the Geographic Site unique within the Seller.")
    
    href: Optional[str] = Field(
        default="",
        description="Unique reference of the Geographic Site unique within the Seller.")
    place: Optional[List[GeographicAddressRefOrValue]] = Field(
        default=None,
        description="A set of location descriptions, each of which describes where this GeographicSite is located. It is important to note that this is a set because a particular Geographic Site might be described with multiple locations. For example, one Geographic Site might have two Fielded Addresses (for a building on the corner of two streets), two Formatted Addresses, and a Geographic Point."
        )
    customerName: Optional[str] = Field(default="",
                                        description="The name of the company that is the administrative authority for the space within this Geographic Site (For example, the company leasing space in a multi-tenant building).")
    siteType : Optional[MEFSiteType] = Field(default="")