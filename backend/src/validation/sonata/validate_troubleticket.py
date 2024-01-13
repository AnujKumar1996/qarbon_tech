def validate_list_troubleticket( json_data, externalId, priority, sellerPriority,
            severity,sellerSeverity, ticketType, status,observedImpact,relatedEntityId,relatedEntityType
            
       ):
    try:
        for item_value in json_data:

            if externalId != "" and externalId != item_value.get("externalId"):
                return False
            
            if priority != "" and priority != item_value.get("priority"):
                return False

            if sellerPriority != "" and sellerPriority != item_value.get("sellerPriority"):
                return False
            
            if severity != "" and severity != item_value.get("severity"):
                return False
            
            if sellerSeverity != "" and sellerSeverity != item_value.get("sellerSeverity"):
                return False
            
            if ticketType != "" and ticketType != item_value.get("ticketType"):
                return False
            
            if status != "" and status != item_value.get("status"):
                return False
            
            if observedImpact != "" and observedImpact != item_value.get("observedImpact"):
                return False
            
            if relatedEntityId != "" and relatedEntityId != item_value["relatedEntity"][0]["id"]:
                return False
            
            if relatedEntityType != "" and relatedEntityType != item_value["relatedEntity"][0]["@referredType"]:
                return False
            
        return True
    except Exception as e:
        return False