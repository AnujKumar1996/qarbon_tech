import json
from pathlib import Path

def map_order_fields(request_data, buyerId, sellerId, ccLoaAttachmentId):
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
                qcl_poid_key = field_json.get("externalId")
                # qcl_poid_val = qcl_src_val.get("poId") #used externalId

                qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_poid_key] = request_data.get("externalId")

                qcl_item_key = field_json.get("itemDetails")

                qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_item_key] = []
                qcl_item_list = qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_item_key]
                
                qcl_item_value = qcl_src_val.get("itemDetails")
                
                for index, item in enumerate(qcl_item_value,1):
                    
                    if not item.get("crossConnectDetails"):
                        status_msg_code = 422
                        message = "'crossConnectDetails' MUST not be empty, when 'action' is set to 'add'"
                        reason = "Validation error"
                        reference_error = "https://docs.pydantic.dev/latest/errors/validation_errors/"
                        message_code = "invalidValue"
                        property_path = None
                        
                        return False, status_msg_code, message, reason, reference_error, message_code, property_path
                    
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

                    cc_details_key = field_json.get("crossConnectDetails")
                    cc_details_val = item.get("crossConnectDetails")

                    item_dict[cc_details_key] = {}
                    
                    request_date_val = cc_details_val.get("ccRequestDate")
                    expedite_time_val = cc_details_val.get("ccExpediteTime")
                    description_val = cc_details_val.get("description")
                    customer_reference_id_val = cc_details_val.get("customerReferenceId")
                    
                    if request_date_val is not None:
                        item_dict[cc_details_key][field_json.get("ccRequestDate")] = str(request_date_val)
                    
                    if expedite_time_val is not None:
                        item_dict[cc_details_key][field_json.get("ccExpediteTime")] = str(expedite_time_val)
                        
                    if description_val is not None:
                        item_dict[cc_details_key][field_json.get("description")] = str(description_val)
                    
                    if customer_reference_id_val is not None:
                        item_dict[cc_details_key][field_json.get("customerReferenceId")] = str(customer_reference_id_val)
                    
                    
                    # fetching aside key and value 
                    aside_key = field_json.get("ccASideDetails")
                    aside_val = cc_details_val.get("ccASideDetails")
                    item_dict[cc_details_key][aside_key] = {}

                    cc_account_id = aside_val.get("ccAccountId")
                    cc_pod_id = aside_val.get("ccPodId")
                    cc_model_id = aside_val.get("ccModelId")
                    cc_port_id = aside_val.get("ccPortId")
                    
                    # fetching zside key and value 
                    zside_key = field_json.get("ccZSideDetails")
                    zside_val = cc_details_val.get("ccZSideDetails")

                    cc_zSideprovider_name = zside_val.get("ccZSideProviderName")

                    if sellerId == "CYX" and not all([cc_account_id, cc_pod_id, cc_model_id, cc_port_id, 
                                                        ccLoaAttachmentId, request_date_val]):
                        
                        statusCode = 422
                        message = "When the sellerId is set to 'CYX,' following fields must be provided: 'ccRequestDate', 'ccAccountId, 'ccPodId', 'ccModelId', 'ccPortId' and 'ccLoaAttachmentId'"
                        reason = "Invalid value"
                        reference_error = "https://example.com/"
                        messageCode = "invalidValue"
                        PropertyPath = "https://tools.ietf.org/html/rfc6901"
                        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
                    
                    if cc_account_id is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccAccountId")] = cc_account_id
                        
                    if cc_pod_id is not None:   
                        item_dict[cc_details_key][aside_key][field_json.get("ccPodId")] = cc_pod_id
                        
                    if cc_model_id is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccModelId")] = cc_model_id
                        
                    if cc_port_id is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccPortId")] = cc_port_id
                    
                
                    cc_asidepatchpanel_id = aside_val.get("ccASidePatchPanelId")
                    cc_connection_service = aside_val.get("ccConnectionService")

                    cc_media_type = aside_val.get("ccMediaType")
                    cc_protocol_type = aside_val.get("ccProtocolType")
                    cc_connector_type = aside_val.get("ccConnectorType")
                    
                    cc_patchpanelport_a = aside_val.get("ccPatchPanelPortA")
                    cc_patchpanelport_b = aside_val.get("ccPatchPanelPortB")
                    
                    cc_ifc_circuit_count = aside_val.get("ccIfcCircuitCount")
                    cc_media_converter_required = aside_val.get("ccMediaConverterRequired")
                    
                    if cc_asidepatchpanel_id is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccASidePatchPanelId")] = cc_asidepatchpanel_id
                    
                    if cc_connection_service is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccConnectionService")] = cc_connection_service
                    
                    if cc_media_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccMediaType")] = cc_media_type
                        
                    if cc_protocol_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccProtocolType")] = cc_protocol_type
                        
                    if cc_connector_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccConnectorType")] = cc_connector_type
                    
                    if cc_patchpanelport_a is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccPatchPanelPortA")] = cc_patchpanelport_a
                    
                    if cc_patchpanelport_b is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccPatchPanelPortB")] = cc_patchpanelport_b

                    if cc_ifc_circuit_count is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccIfcCircuitCount")] = cc_ifc_circuit_count
                        
                    if cc_media_converter_required is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccMediaConverterRequired")] = cc_media_converter_required
                    
                    patch_panel_equipment_details_val = aside_val.get("ccPatchEquipmentDetails")
                    
                    if patch_panel_equipment_details_val is not None:
                        patch_panel_equipment_details_key = field_json.get("ccPatchEquipmentDetails")
                        item_dict[cc_details_key][aside_key][patch_panel_equipment_details_key] = {}

        
                    # Validate zside required fields for EQX        
                    cc_zconnector_type = zside_val.get("ccConnectorType")
                    
                    cc_zpatchpanelport_a = zside_val.get("ccPatchPanelPortA")
                    cc_zpatchpanelport_b = zside_val.get("ccPatchPanelPortB")
                    
                    cc_circuit_id = zside_val.get("ccCircuitId")
                    notification_email = zside_val.get("notificationEmail")
                    
                    
                    if sellerId == "EQX" and not all([cc_asidepatchpanel_id, cc_connection_service, cc_media_type,
                            cc_protocol_type, cc_connector_type]):
                                            
                
                        statusCode = 422
                        message = "When the sellerId is set to 'EQX,' following fields must be provided: 'ccASidePatchPanelId', 'ccConnectionService', 'ccMediaType', 'ccProtocolType', 'ccConnectorType' and 'ccZSidePatchPanelId'"
                        reason = "Invalid value"
                        reference_error = "https://example.com/"
                        messageCode = "invalidValue"
                        PropertyPath = "https://tools.ietf.org/html/rfc6901"
                        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
                                        
                    if cc_asidepatchpanel_id is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccASidePatchPanelId")] = cc_asidepatchpanel_id
                    
                    if cc_connection_service is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccConnectionService")] = cc_connection_service

                    if cc_media_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccMediaType")] = cc_media_type
                        
                    if cc_protocol_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccProtocolType")] = cc_protocol_type
                        
                    if cc_connector_type is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccConnectorType")] = cc_connector_type
                    
                    if cc_patchpanelport_a is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccPatchPanelPortA")] = cc_patchpanelport_a
                    
                    if cc_patchpanelport_b is not None:
                        item_dict[cc_details_key][aside_key][field_json.get("ccPatchPanelPortB")] = cc_patchpanelport_b
                    
                    cc_zsidepatchpanel_id = zside_val.get("ccZSidePatchPanelId")


                    if patch_panel_equipment_details_val is not None:  
                        pe_cabinet_id = patch_panel_equipment_details_val.get("peCabinetId")
                        pe_connector_type = patch_panel_equipment_details_val.get("peConnectorType")
                        pe_additional_details = patch_panel_equipment_details_val.get("peAdditionalDetails")
                        pe_port = patch_panel_equipment_details_val.get("pePort")
                        
                    
                        if pe_cabinet_id is not None :
                            item_dict[cc_details_key][aside_key][patch_panel_equipment_details_key][field_json.get("peCabinetId")] = pe_cabinet_id
                            
                        if pe_connector_type is not None:
                            item_dict[cc_details_key][aside_key][patch_panel_equipment_details_key][field_json.get("peConnectorType")] = pe_connector_type
                            
                        if pe_additional_details is not None:
                            item_dict[cc_details_key][aside_key][patch_panel_equipment_details_key][field_json.get("peAdditionalDetails")] = pe_additional_details
                            
                        if pe_port is not None:  
                            item_dict[cc_details_key][aside_key][patch_panel_equipment_details_key][field_json.get("pePort")] = pe_port
                        
                    item_dict[cc_details_key][zside_key] = {}
                    

                    cc_ibx = zside_val.get("ccIbx")
                    
                    if cc_zSideprovider_name is not None:
                        item_dict[cc_details_key][zside_key][field_json.get("ccZSideProviderName")] = cc_zSideprovider_name
                    
                    item_dict[cc_details_key][zside_key][field_json.get("ccZSidePatchPanelId")] = cc_zsidepatchpanel_id                
                    item_dict[cc_details_key][zside_key][field_json.get("ccConnectorType")] = cc_zconnector_type
                                        
                    if cc_ibx is not None:
                        item_dict[cc_details_key][zside_key][field_json.get("ccIbx")] = cc_ibx
                    
                    item_dict[cc_details_key][zside_key][field_json.get("ccPatchPanelPortA")] = cc_zpatchpanelport_a
                    item_dict[cc_details_key][zside_key][field_json.get("ccPatchPanelPortB")] = cc_zpatchpanelport_b
                    
                    if cc_circuit_id is not None:
                        item_dict[cc_details_key][zside_key][field_json.get("ccCircuitId")] = cc_circuit_id
                    
                    if notification_email is not None:
                        item_dict[cc_details_key][zside_key][field_json.get("notificationEmail")] = notification_email
                        
                    cc_diverse_connection_details_key = field_json.get("ccDiverseConnectionDetails")
                    diverse_connection_details_val = cc_details_val.get("ccDiverseConnectionDetails")
                    item_dict[cc_details_key][cc_diverse_connection_details_key] = {}                    

                    if diverse_connection_details_val is not None:

                        dc_type = diverse_connection_details_val.get("dcType")
                        dc_serial_number = diverse_connection_details_val.get("dcSerialNumber")
                    
                        if dc_type is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][field_json.get("dcType")] =  dc_type            
                        
                        if dc_serial_number is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][field_json.get("dcSerialNumber")] = dc_serial_number
                        
                    
                        dc_a_side_details_key = field_json.get("dcASideDetails")
                        dc_a_side_details_val = diverse_connection_details_val.get("dcASideDetails")
                        item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key] = {}
                                        
                        dc_patch_panel_details_key = field_json.get("dcPatchPanelDetails")
                        dc_patch_panel_details_val = dc_a_side_details_val.get("dcPatchPanelDetails")
                        item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_panel_details_key] = {}
                        
                        
                        dc_patch_panel_id = dc_patch_panel_details_val.get("dcPatchPanelId")
                        dc_patch_panel_port_a = dc_patch_panel_details_val.get("dcPatchPanelPortA")
                        dc_patch_panel_port_b = dc_patch_panel_details_val.get("dcPatchPanelPortB")
                        
                        if dc_patch_panel_id is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelId")] = dc_patch_panel_id
                        if dc_patch_panel_port_a is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelPortA")] = dc_patch_panel_port_a
                        if dc_patch_panel_port_b is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelPortB")] = dc_patch_panel_port_b
                        
                    
                        dc_connector_type = dc_a_side_details_val.get("dcConnectorType")
                        dc_media_converter_required = dc_a_side_details_val.get("dcMediaConverterRequired")
                        dc_ifc_circuit_count = dc_a_side_details_val.get("dcIfcCircuitCount")
                        
                        if dc_connector_type is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][field_json.get("dcConnectorType")] = dc_connector_type
                            
                        if dc_media_converter_required is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][field_json.get("dcMediaConverterRequired")] = dc_media_converter_required
                            
                        if dc_ifc_circuit_count is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][field_json.get("dcIfcCircuitCount")] = dc_ifc_circuit_count
                        
                        dc_patch_equipment_key = field_json.get("dcPatchEquipment")
                        dc_patch_equipment_val = dc_a_side_details_val.get("dcPatchEquipment")
                        item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key] = {}
                        
                        pe_cabinet_id = dc_patch_equipment_val.get("peCabinetId")
                        pe_connector_type = dc_patch_equipment_val.get("peConnectorType")
                        pe_details = dc_patch_equipment_val.get("peDetails")
                        pe_port = dc_patch_equipment_val.get("pePort")
                        pe_additional_details = dc_patch_equipment_val.get("peAdditionalDetails")
                        
                        if pe_cabinet_id is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key][field_json.get("peCabinetId")] = pe_cabinet_id 
                        if pe_connector_type is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key][field_json.get("peConnectorType")] = pe_connector_type
                        if pe_details is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key][field_json.get("peDetails")] = pe_details
                        if pe_port is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key][field_json.get("pePort")] = pe_port
                        if pe_additional_details is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_a_side_details_key][dc_patch_equipment_key][field_json.get("peAdditionalDetails")] = pe_additional_details

                        dc_z_side_details_key = field_json.get("dcZSideDetails")
                        dc_z_side_details_val = cc_details_val.get("ccDiverseConnectionDetails").get("dcZSideDetails")
                        item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key] = {}
                        
                        dc_patch_panel_details_key = field_json.get("dcPatchPanelDetails")
                        z_side_dc_patch_panel_details_val = dc_z_side_details_val.get("dcPatchPanelDetails")
                        item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][dc_patch_panel_details_key] = {}
                        
                        dc_patch_panel_id = z_side_dc_patch_panel_details_val.get("dcPatchPanelId")
                        dc_patch_panel_port_a = z_side_dc_patch_panel_details_val.get("dcPatchPanelPortA")
                        dc_patch_panel_port_b = z_side_dc_patch_panel_details_val.get("dcPatchPanelPortB")
                        
                        if dc_patch_panel_id is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelId")] = dc_patch_panel_id
                        if dc_patch_panel_port_a is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelPortA")] = dc_patch_panel_port_a
                        if dc_patch_panel_port_b is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][dc_patch_panel_details_key][field_json.get("dcPatchPanelPortB")] = dc_patch_panel_port_b
                        
                        dc_connector_type = dc_z_side_details_val.get("dcConnectorType")
                        dc_circuit_id = dc_z_side_details_val.get("dcIfcCircuitId")
                        
                        
                        if dc_connector_type is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][field_json.get("dcConnectorType")] = dc_connector_type
                        if dc_circuit_id is not None:
                            item_dict[cc_details_key][cc_diverse_connection_details_key][dc_z_side_details_key][field_json.get("dcIfcCircuitId")] = dc_circuit_id
                        
                        cc_verify_link = cc_details_val.get("ccVerifyLink")
                        cc_circuit_delivery_date = cc_details_val.get("ccCircuitDeliveryDate")
                        cc_submarine_engineer_required = cc_details_val.get("ccSubmarineEngineerRequired")
                        
                        if cc_verify_link is not None:
                            item_dict[cc_details_key][field_json.get("ccVerifyLink")] = cc_verify_link
                        if cc_circuit_delivery_date is not None:
                            item_dict[cc_details_key][field_json.get("ccCircuitDeliveryDate")] = cc_circuit_delivery_date
                        if cc_submarine_engineer_required is not None:
                            item_dict[cc_details_key][field_json.get("ccSubmarineEngineerRequired")] = cc_submarine_engineer_required
                        
                        
                        attachment_details_key = field_json.get("attachmentDetails")
                        attachment_details_val = cc_details_val.get("attachmentDetails")
                        item_dict[cc_details_key][attachment_details_key] = [{}]
                        
                        
                        for attach_val in attachment_details_val:
                            
                            attachment_id = ccLoaAttachmentId
                            attachment_name = attach_val["attachmentName"]
                            
                            
                            if attachment_id is not None:
                                item_dict[cc_details_key][attachment_details_key][0][field_json.get("ccattachmentId")] = attachment_id
                            if attachment_name is not None:
                                item_dict[cc_details_key][attachment_details_key][0][field_json.get("attachmentName")] = attachment_name
                            
                        purchase_order_details_key = field_json.get("purchaseOrderDetails")
                        purchase_order_details_val = cc_details_val.get("purchaseOrderDetails")
                        item_dict[cc_details_key][purchase_order_details_key] = {}
                        
                        po_type = purchase_order_details_val.get("poType")
                        po_number = purchase_order_details_val.get("poNumber")
                        po_amount = purchase_order_details_val.get("poAmount")
                        po_start_date = purchase_order_details_val.get("poStartDate")
                        po_end_date = purchase_order_details_val.get("poEndDate")
                        qcl_attachment_id = ccLoaAttachmentId
                        #purchase_order_details_val.get("ccattachmentId")
                        
                        
                        if po_type is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("poType")] = po_type
                            
                        if po_number is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("poNumber")] = po_number
                            
                        if po_amount is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("poAmount")] = po_amount
                            
                        if po_start_date is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("poStartDate")] = po_start_date
                        
                        if po_end_date is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("poEndDate")] = po_end_date
                            
                        if qcl_attachment_id is not None:
                            item_dict[cc_details_key][purchase_order_details_key][field_json.get("ccattachmentId")] = qcl_attachment_id
                        
                        contacts_key = field_json.get("contacts")
                        
                        item_dict[cc_details_key][contacts_key] = [{}]
                        
                        south_username_key = field_json.get("southUsername")
                        south_username_val = cc_details_val.get("contacts")[0].get("southUsername")
                                        
                        item_dict[cc_details_key][contacts_key][0][south_username_key] = [south_username_val[0]]
                        
                        contacts_val = cc_details_val.get("contacts")[0]
                                        
                        first_name = contacts_val.get("firstName")
                        last_name = contacts_val.get("lastName")
                        contact_type = contacts_val.get("contactType")
                        availability = contacts_val.get("availability")
                        timezone = contacts_val.get("timezone")
                        
                        if first_name is not None:
                            item_dict[cc_details_key][contacts_key][0][field_json.get("firstName")] = first_name
                        if last_name is not None:
                            item_dict[cc_details_key][contacts_key][0][field_json.get("lastName")] = last_name
                        if contact_type is not None:
                            item_dict[cc_details_key][contacts_key][0][field_json.get("contactType")] = contact_type
                        if availability is not None:
                            item_dict[cc_details_key][contacts_key][0][field_json.get("availability")] = availability
                        if timezone is not None:
                            item_dict[cc_details_key][contacts_key][0][field_json.get("timezone")] = timezone
                            
                        
                        notification_details_key = field_json.get("notificationDetails")
                        notification_details_value = contacts_val.get("notificationDetails")[0]                        

                        if notification_details_value is not None:
                            item_dict[cc_details_key][contacts_key][0][notification_details_key] = [{}]
                            type = notification_details_value.get("type")
                            value =  notification_details_value.get("value")
                            
                            
                            if type is not None:                              
                                item_dict[cc_details_key][contacts_key][0][notification_details_key][0][field_json.get("type")] = type
                            
                            if value is not None:
                                item_dict[cc_details_key][contacts_key][0][notification_details_key][0][field_json.get("value")] = value
                            
                    if ccLoaAttachmentId is not None:
                        item_dict[cc_details_key][zside_key][field_json.get("ccLoaAttachmentId")] = ccLoaAttachmentId

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
    