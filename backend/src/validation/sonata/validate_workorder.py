def validate_list_workorder(json_data, relatedEntityType, relatedEntityId, state, appointmentRequired):
    try:        
        for item_value in json_data:
            if appointmentRequired is not None:
                item_appointmentRequired = item_value.get(
                    "appointmentRequired")
                if appointmentRequired != item_appointmentRequired:
                    return False

            if state != "":
                item_state = item_value.get("state")
                if state != item_state:
                    return False

            if relatedEntityType != "":
                item_relatedEntity = item_value.get("relatedEntity")
                for entity in item_relatedEntity:
                    referredType = entity.get("@referredType", "")
                    if referredType != relatedEntityType:
                        return False

            if relatedEntityId != "":
                item_relatedEntity = item_value.get("relatedEntity")
                for entity in item_relatedEntity:
                    relatedId = entity.get("id", "")
                    if relatedEntityId != relatedId:
                        return False

        return True
    except Exception:
        return False


def validate_workorder_by_id(response_data, id):
    try:
        if response_data.get("id") != id:
            return False
        return True
    except Exception as e:
        return False