from pathlib import Path
import json
from fastapi import status
from src.common.exceptions import raise_exception
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.sonata_schemas.geographicsitemanagement_schema import GeographicSite
from src.validation.sonata.validate_geographicsite_list import validate_geographicsite_list

def  retrieve_geographicsite_list(country,postcode,city,
                                  streetType,streetName,
                                  streetNr,geographicAddress_id,
                                  serviceSiteContactName,name,
                                  siteType,description,customerName,
                                  companyName,buyerId, sellerId):
   
    """
    This function retrieves a geographicsite by List.
    """
    
    try:
        
        current_directory = Path(__file__).parents[1]
        response_file = "geographicsitemanagement_geographicsite.json"
        file_name = current_directory / 'responses'/response_file
            
        if not file_name.exists():
            return raise_exception(status_msg_code=404,
                                    message=f"File not found '{response_file}'",
                                    reason="File not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)
        try:
            with open(file_name,'r') as json_file:
                json_data = json.load(json_file)

        except json.JSONDecodeError as e:
            return raise_exception(status_msg_code=404, 
                                    message="Record not found", 
                                    reason="Record not found", 
                                    reference_error=None, 
                                    message_code="notFound", 
                                    property_path=None)   
        
        
        extracted_data = []
        
        for _, geographicsite_info in json_data.items():
                
            json_relatedcontactInfo = geographicsite_info.get("relatedContactInformation")
            json_city = None
            json_postcode = None
            json_streettype = None
            json_country=None
            json_streetnr  = None
            json_streetname  = None
            json_postaladress=None
            if json_relatedcontactInfo is not None:
                for item in json_relatedcontactInfo:
                    json_postaladress = item.get("postalAddress")
                    if json_postaladress is not None:
                       json_city=json_postaladress.get('city')
                       json_country=json_postaladress.get('country')
                       json_postcode=json_postaladress.get('postcode')
                       json_streettype=json_postaladress.get('streetType')
                       json_streetnr=json_postaladress.get('streetNr')
                       json_streetname=json_postaladress.get('streetName')



            json_companyname = geographicsite_info.get("companyName")
            json_name = geographicsite_info.get("name")
            json_description = geographicsite_info.get("description")
            json_customername = geographicsite_info.get("customerName")
            json_sitetype = geographicsite_info.get("siteType")
            json_servicesitecontactName = geographicsite_info.get("serviceSiteContactName")
            json_geographicaddress_id = geographicsite_info.get("geographicAddress_id")
            json_buyerid = geographicsite_info.get("buyerId")
            json_sellerid = geographicsite_info.get("sellerId")
        
            if ((city == "" or city == json_city) and
                (postcode == ""  or postcode == json_postcode) and
                (country == ""  or country == json_country) and
                (streetNr == "" or streetNr == json_streetnr) and
                (streetName == ""  or streetName == json_streetname) and
                (streetType == ""  or streetType == json_streettype) and
                (name == ""  or name == json_name) and
                (description == ""  or description == json_description) and
                (customerName == ""  or customerName == json_customername) and
                (siteType == "" or siteType == json_sitetype) and
                (serviceSiteContactName == ""  or serviceSiteContactName == json_servicesitecontactName) and
                (geographicAddress_id == ""  or geographicAddress_id == json_geographicaddress_id) and
                (companyName == ""  or companyName == json_companyname) and
                (buyerId == ""  or buyerId == json_buyerid) and
                (sellerId == ""  or sellerId == json_sellerid)
                ):
                extracted_info = {
                   
                    "companyName": geographicsite_info.get("companyName"),
                    "name": geographicsite_info.get("name"),
                    "description": geographicsite_info.get("description"),
                    "customerName": geographicsite_info.get("customerName"),
                    "siteType": geographicsite_info.get("siteType"),
                    "serviceSiteContactName": geographicsite_info.get("serviceSiteContactName"),
                    "relatedContactInformation":geographicsite_info.get("relatedContactInformation"),
                    "id":geographicsite_info.get("id"),
                    "href":geographicsite_info.get("href"),
                    "place":geographicsite_info.get("place")
                    
                }
                
                extracted_data.append(extracted_info)
        limited_responses = extracted_data   

        if not limited_responses or not extracted_data:
                status_msg_code = 404
                message = "No matching result found for the given criteria."
                reason = "Record not found"
                reference_error = None
                message_code = "notFound"
                property_path = None
                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
            
        limited_responses_schema = [GeographicSite(**response) for response in limited_responses]
        json_data = jsonable_encoder(limited_responses_schema)
        
        
        is_validated= validate_geographicsite_list(json_data,companyName, name, description,streetType,
                                                  customerName,siteType,city,country,postcode,streetNr,streetName)

        if not is_validated:
            
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

           
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=json_data,
                media_type="application/json;charset=utf-8")
    
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
  