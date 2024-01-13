import json
from pathlib import Path


def map_deinstall_fields(request_data, buyerId, sellerId,ccLoaAttachmentId):
    """
    Function for field mapping between MEF and QCL.

    In case of an error, it returns:
        - False*: Indicates a failure to map the fields.
        - statusCode*: Specifies the HTTP status code for the error.
        - message*: Provides a message describing the error.
        - reason*: Indicates the reason for the error.
        - reference_error: URL pointing to documentation explaining the error.
        - messageCode*: A code associated with the error.
        - PropertyPath: Only applicable in the case of a 422 error.

    Otherwise, it returns:
        - True*: Signifies successful field mapping.
        - resultDict: Contains the mapped payload.
    """

    try:
        current_directory = Path(__file__).parents[1]
        file_name = 'field_mapping.json'
        field_map_file_name = current_directory / 'common' / file_name

        if not field_map_file_name.exists():
            
            statusCode = 404
            message = f"{file_name} file not found"
            reason = "File not found"
            reference_error = "https://pythonguides.com/file-does-not-exist-python/"
            messageCode = "notFound"
            PropertyPath = None
            return False, statusCode, message, reason, reference_error, messageCode, PropertyPath

        try:
            with open(field_map_file_name, "r") as json_file:
                json_data = json.load(json_file)
        
        except json.JSONDecodeError as e: 
            
            statusCode = 404
            message = "Record not found in field_mapping.json file"
            reason = "Record not found"
            reference_error = "https://pythonguides.com/file-does-not-exist-python/"
            messageCode = "notFound"
            PropertyPath = None
            return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
        
        field_json = json_data.get("qcl_cc_order")
        qcl_request_dict = {}
        transaction_data = request_data.get("transactionData")

        if transaction_data:
            qcl_gereric_data_key = field_json.get("qclGenericData")
            qcl_source_key = field_json.get("buyerId")
            qcl_dest_key = field_json.get("sellerId")

            if qcl_gereric_data_key and qcl_dest_key and qcl_source_key:
                qcl_request_dict.update(
                    {
                        qcl_gereric_data_key: {
                                qcl_source_key: buyerId,
                                qcl_dest_key: sellerId
                            }
                        })

                qcl_transaction_key = field_json.get("transactionData")
                qcl_generic_field_key = field_json.get("genericFields")
                qcl_dest_field_key = field_json.get("destinationFields")
                qcl_src_field_key = field_json.get("sourceFields")

                qcl_request_dict.update(
                    {
                        qcl_transaction_key: {
                            qcl_generic_field_key: transaction_data.get("genericFields"),
                            qcl_dest_field_key: transaction_data.get("destinationFields"),
                            qcl_src_field_key: {}  
                        }
                    })
                
                
                qcl_src_val = transaction_data.get("sourceFields")
                qcl_iaid_key = field_json.get("iaId")
                qcl_iaId_val = qcl_src_val.get("iaId")
                
                if qcl_iaId_val is None:
                    status_msg_code = 422
                    message = "'iaId' MUST not be empty, when 'action' is set to 'delete'"
                    reason = "Validation error"
                    reference_error = "https://docs.pydantic.dev/latest/errors/validation_errors/"
                    message_code = "invalidValue"
                    property_path = None
                    
                    return False, status_msg_code, message, reason, reference_error, message_code, property_path
                
                qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_iaid_key] = qcl_iaId_val
                qcl_item_key = field_json.get("itemDetails")

                qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_item_key] = []
                qcl_item_list = qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_item_key]
                
                qcl_item_value = qcl_src_val.get("itemDetails")
                for index, item in enumerate(qcl_item_value,1):
                    item_dict = {}

                    productorderitem_length = len(request_data.get("productOrderItem"))
                    if index > productorderitem_length:
                        
                        statusCode = 422
                        message = "Number of itemDetails must not exceed number of productOrderItem"
                        reason = "Too many records"
                        reference_error = "https://example.com/"
                        messageCode = "tooManyRecords"
                        PropertyPath = "https://tools.ietf.org/html/rfc6901"
                        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath

                    item_dict[field_json.get("productOrderItemId")] = request_data.get("productOrderItem")[index-1]["id"]

                    if item.get("inventoryItemName") != "Cross Connect":
                        
                        statusCode = 422
                        message = "inventoryItemName should be 'Cross Connect'"
                        reason = "Invalid value"
                        reference_error = "https://example.com/"
                        messageCode = "invalidValue"
                        PropertyPath = "https://tools.ietf.org/html/rfc6901"
                        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
                    
                    item_dict[field_json.get("inventoryItemName")] = item.get("inventoryItemName")
                    
                    original_item_key = field_json.get("originalItemDetails")
                    item_dict[original_item_key] = item.get("originalItemDetails")

                    cc_deinstall_key = field_json.get("ccDeinstallDetails")
                    cc_deinstall_val = item.get("ccDeinstallDetails")

                    if cc_deinstall_val is None:
                        status_msg_code = 422
                        message = "'ccDeinstallDetails' MUST not be empty, when 'action' is set to 'delete'"
                        reason = "Validation error"
                        reference_error = "https://docs.pydantic.dev/latest/errors/validation_errors/"
                        message_code = "invalidValue"
                        property_path = None
                        
                        return False, status_msg_code, message, reason, reference_error, message_code, property_path
                    
                    item_dict[cc_deinstall_key] = {}
                    item_dict[cc_deinstall_key][field_json.get("ccDeinstallId")] = cc_deinstall_val.get("ccDeinstallId")
                    item_dict[cc_deinstall_key][field_json.get("ccRemovalDate")] = str(cc_deinstall_val.get("ccRemovalDate"))
                    
                    customer_refrence_id = cc_deinstall_val.get("customerReferenceId")
                    description = cc_deinstall_val.get("description")
                    
                    if customer_refrence_id is not None:
                        item_dict[cc_deinstall_key][field_json.get("customerReferenceId")] = cc_deinstall_val.get("customerReferenceId")
                        
                    if description is not None:
                        item_dict[cc_deinstall_key][field_json.get("description")] = str(cc_deinstall_val.get("description"))
                    
                    patch_equipment_details_key = field_json.get("ccPatchEquipmentDetails")
                    patch_equipment_details_val = cc_deinstall_val.get("ccPatchEquipmentDetails")
                    
                                        
                    if patch_equipment_details_val is not None:  
                        
                        item_dict[cc_deinstall_key][patch_equipment_details_key] = {}
                        pe_cabinet_id = patch_equipment_details_val.get("peCabinetId")
                        pe_additional_details = patch_equipment_details_val.get("peAdditionalDetails")
                        pe_port = patch_equipment_details_val.get("pePort")
                        
                    
                        if pe_cabinet_id is not None :
                            item_dict[cc_deinstall_key][patch_equipment_details_key][field_json.get("peCabinetId")] = pe_cabinet_id
                            
                        if pe_additional_details is not None:
                            item_dict[cc_deinstall_key][patch_equipment_details_key][field_json.get("peAdditionalDetails")] = pe_additional_details
                                
                        if pe_port is not None:  
                            item_dict[cc_deinstall_key][patch_equipment_details_key][field_json.get("pePort")] = pe_port
                        
                        attachment_details_key = field_json.get("attachmentDetails")
                        attachment_details_val = cc_deinstall_val.get("attachmentDetails")
                        item_dict[cc_deinstall_key][attachment_details_key] = [{}]
                        
                        for attach_val in attachment_details_val:
                    
                            attachment_id = ccLoaAttachmentId
                            attachment_name = attach_val["attachmentName"]
                            
                            
                            if attachment_id is not None:
                                item_dict[cc_deinstall_key][attachment_details_key][0][field_json.get("ccattachmentId")] = attachment_id
                            if attachment_name is not None:
                                item_dict[cc_deinstall_key][attachment_details_key][0][field_json.get("attachmentName")] = attachment_name
                                
                            purchase_order_details_key = field_json.get("purchaseOrderDetails")
                            purchase_order_details_val = cc_deinstall_val.get("purchaseOrderDetails")
                            item_dict[cc_deinstall_key][purchase_order_details_key] = {}
                            
                            po_type = purchase_order_details_val.get("poType")
                            po_number = purchase_order_details_val.get("poNumber")
                            po_amount = purchase_order_details_val.get("poAmount")
                            po_start_date = purchase_order_details_val.get("poStartDate")
                            po_end_date = purchase_order_details_val.get("poEndDate")
                            qcl_attachment_id = ccLoaAttachmentId
                            
                            if po_type is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("poType")] = po_type
                                    
                            if po_number is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("poNumber")] = po_number
                                
                            if po_amount is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("poAmount")] = po_amount
                                
                            if po_start_date is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("poStartDate")] = po_start_date
                            
                            if po_end_date is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("poEndDate")] = po_end_date
                                
                            if qcl_attachment_id is not None:
                                item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("ccattachmentId")] = qcl_attachment_id
                    
                            proceed_with_live_traffic = cc_deinstall_val.get("proceedWithLiveTraffic")
                            item_dict[cc_deinstall_key][purchase_order_details_key][field_json.get("proceedWithLiveTraffic")] = proceed_with_live_traffic
                            
                            contacts_key = field_json.get("contacts")
                    
                            item_dict[cc_deinstall_key][contacts_key] = [{}]
                            
                            south_username_key = field_json.get("southUsername")
                            south_username_val = cc_deinstall_val.get("contacts")[0].get("southUsername")
                                            
                            item_dict[cc_deinstall_key][contacts_key][0][south_username_key] = [south_username_val[0]]
                            
                            contacts_val = cc_deinstall_val.get("contacts")[0]
                                            
                            first_name = contacts_val.get("firstName")
                            last_name = contacts_val.get("lastName")
                            contact_type = contacts_val.get("contactType")
                            availability = contacts_val.get("availability")
                            timezone = contacts_val.get("timezone")
                            
                            if first_name is not None:
                                item_dict[cc_deinstall_key][contacts_key][0][field_json.get("firstName")] = first_name
                            if last_name is not None:
                                item_dict[cc_deinstall_key][contacts_key][0][field_json.get("lastName")] = last_name
                            if contact_type is not None:
                                item_dict[cc_deinstall_key][contacts_key][0][field_json.get("contactType")] = contact_type
                            if availability is not None:
                                item_dict[cc_deinstall_key][contacts_key][0][field_json.get("availability")] = availability
                            if timezone is not None:
                                item_dict[cc_deinstall_key][contacts_key][0][field_json.get("timezone")] = timezone
                            
                    qcl_item_list.append(item_dict)
            return True, 200, qcl_request_dict, None, None, None, None
        
    except Exception as e:
        
        statusCode = 500
        message =  str(e)
        reason = "Invalid value"
        reference_error = None
        messageCode = "internalError"
        PropertyPath = None
        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
    