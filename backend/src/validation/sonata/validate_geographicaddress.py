

def validate_geographicaddress(response_data, request_data):
    """
    validating geographicaddress response     
    """
    if request_data.get("submittedGeographicAddress", {}).get("associatedGeographicAddress") is not None:

        response_associated_geographic_address = response_data.get("submittedGeographicAddress", {}).get("associatedGeographicAddress", {})
        request_associated_geographic_address = request_data.get("submittedGeographicAddress", {}).get("associatedGeographicAddress", {})
        
       
        if response_associated_geographic_address != request_associated_geographic_address:
            return False

    return True


    