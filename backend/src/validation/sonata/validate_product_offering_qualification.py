def validate_list_product_offering_qualification(json_data, state, externalId, projectId, requestedPOQCompletionDate_gt, requestedPOQCompletionDate_lt, buyerId, sellerId):
    try:
        for item_value in json_data:
            if state != "" and state != item_value.get("state"):
                return False

            if externalId != "" and externalId != item_value.get("externalId"):
                return False

            if projectId != "" and projectId != item_value.get("projectId"):
                return False

            if requestedPOQCompletionDate_gt != None and (requestedPOQCompletionDate_gt and not requestedPOQCompletionDate_gt <= item_value.get("requestedPOQCompletionDate")):
                return False
            
            if requestedPOQCompletionDate_lt != None and (requestedPOQCompletionDate_lt and not requestedPOQCompletionDate_lt >= item_value.get("requestedPOQCompletionDate")):
                return False

        return True
    except Exception as e:
        return False
    
def validate_poq_by_id(response_data, id):
    try:
        if response_data.get("id") != id:
            return False
        return True
    except Exception as e:
        return False

def validate_by_id(response_data, id):
    try:
        if response_data.get("id") != id:
            return False
        return True
    except Exception as e:
        return False