

def validate_geographicsite_list(json_data,companyName, name, description,streetType,
                                customerName,siteType,city,country,
                                postcode,streetNr,streetName):
    
    for item_value in json_data:
            if companyName !="":
                item_companyname = item_value.get(
                    "companyName")
                if item_companyname !="":
                    if companyName != item_companyname:
                        return False
                
            if name !="":
                item_name= item_value.get("name") 
                if item_name !="":
                    if name !=item_name:
                        return False
            
            if description !="":
                item_description= item_value.get("description") 
                if item_description !="":
                    if description !=item_description:
                        return False         

            if customerName !="":
                item_customername= item_value.get("customerName") 
                if item_customername !="":
                    if customerName !=item_customername:
                        return False
                    
            if siteType !="":
                item_sitetype= item_value.get("siteType") 
                if item_sitetype !="":
                    if siteType !=item_sitetype:
                        return False  
            
            
            json_relatedcontactinformation= item_value.get("relatedContactInformation") 
            if json_relatedcontactinformation is not None:
                for item in json_relatedcontactinformation:
                    json_postaladress = item.get("postalAddress")
                    if  json_postaladress is not None:
                        json_city=json_postaladress.get('city')
                        json_country=json_postaladress.get('country')
                        json_postcode=json_postaladress.get('postcode')
                        json_streettype=json_postaladress.get('streetType')
                        json_streetnr=json_postaladress.get('streetNr')
                        json_streetname=json_postaladress.get('streetName')   
                     
                        if city !="":
                            if city !=json_city:
                                    return False  
                        
                        if country !="":
                            if country !=json_country:
                                    return False  
                        
                        if postcode  !="":
                            if json_postcode !="":
                                if postcode !=json_postcode:
                                        return False  
                        
                        if streetType !="":
                            if json_streettype !="":
                                if streetType !=json_streettype:
                                        return False  
                        
                        if streetNr !="":
                            if json_streetnr !="":
                                if streetNr !=json_streetnr:
                                        return False  
                        
                        if streetName !="":
                            if json_streetname !="":
                                if streetName !=json_streetname:
                                        return False                      
                            
                            
    return True                        