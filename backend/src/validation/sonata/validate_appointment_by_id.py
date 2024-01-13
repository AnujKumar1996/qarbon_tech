

def validate_appointment_by_id(json_data,workOrderId, appointment_status ):
    
    for item_value in json_data:
            if workOrderId != "":
                item_workOrderId = item_value.get("workOrder").get("id")
                if workOrderId != item_workOrderId:
                    return False

            if appointment_status != "":
                item_status = item_value.get("status")
                if appointment_status != item_status:
                    return False
    return True          