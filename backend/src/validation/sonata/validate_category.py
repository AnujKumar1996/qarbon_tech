def validate_list_category(json_data, parentCategory_name, lifecycleStatus):
    try:
        for item in json_data:
            if parentCategory_name != "":
                name = item.get("name")
                if parentCategory_name != name:
                    return False    
            if lifecycleStatus != "":
                status = item.get("lifecycleStatus")
                if lifecycleStatus != status:
                    return False    
        return True
    except Exception as e:
        return False

def validate_category(json_data, id):
    try:
        for item in json_data:
            if id != "":
                category_id = json_data.get(item).get("id")
                if id == category_id:
                    return True    
        return False
    except Exception as e:
        return False
