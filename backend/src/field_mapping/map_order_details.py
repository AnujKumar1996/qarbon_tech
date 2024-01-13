
from src.common.json_read import field_mapping_key_val


def map_order_details_fields(request_data):
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
        
        json_data = field_mapping_key_val
        field_json = json_data.get("qcl_cc_order")
        qcl_request_dict = {}

        transaction_data = request_data.get("transactionData")
        generic_data = request_data.get("genericData")

        if transaction_data and generic_data:
            qcl_gereric_data_key = field_json.get("qclGenericData")
            qcl_source_key = field_json.get("sourceId")
            qcl_dest_key = field_json.get("destinationId")

            qcl_source_val = generic_data.get("sourceId")
            qcl_dest_val = generic_data.get("destinationId")
            
            if qcl_gereric_data_key and qcl_dest_key and qcl_source_key:
                qcl_request_dict.update(
                    {
                        qcl_gereric_data_key: {
                                qcl_source_key: qcl_source_val,
                                qcl_dest_key: qcl_dest_val
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
                qcl_order_id_key = field_json.get("orderId")
                qcl_order_id_val = qcl_src_val.get("orderId")
                                
                qcl_request_dict[qcl_transaction_key][qcl_src_field_key][qcl_order_id_key] = qcl_order_id_val
                                
            return True, 200, qcl_request_dict, None, None, None, None
    
    except Exception as e:
        
        statusCode = 500
        message =  str(e)
        reason = "Invalid value"
        reference_error = None
        messageCode = "internalError"
        PropertyPath = None
        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
    
