

def validate_customer_bill_by_list(json_data, billingAccount_id, category, state):
                       
    for item_value in json_data:
        
        if billingAccount_id !="":
            if item_value.get("billingAccount") is not None:
                item_billingAccount_id = item_value.get("billingAccount").get("id")
                
                if item_billingAccount_id !="":
                    if billingAccount_id != item_billingAccount_id:
                        return False
                
        if category !="":
            item_category= item_value.get("category") 
            if item_category !="":
                if category !=item_category:
                    return False
        
        if state !="":
            item_state= item_value.get("state") 
            if item_state !="":
                if state !=item_state:
                    return False         

    return True      