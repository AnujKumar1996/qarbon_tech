from src.common.json_read import field_mapping_key_val
from src.common.convert_to_date_format import convert_to_date_format

def map_cc_list_fields(buyerId, sellerId, offset, limit, orderDate_gt, orderDate_lt):
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
        if orderDate_gt is None and orderDate_lt is None:
                    
            json_data = {

                "qcl_generic_data": {
                    "qcl_source_id": buyerId,
                    "qcl_destination_id": sellerId
                },
                "qcl_transaction_data": {
                    "generic_fields": {},
                    "source_fields": {
                        "offset": offset,
                        "limit": limit
                    },
                    "destination_fields": {}
            }
                }
        else:
            if orderDate_gt is not None:
                parsed_orderdate_gt = convert_to_date_format(orderDate_gt)
            if orderDate_lt is not None:
                parsed_orderdate_lt = convert_to_date_format(orderDate_lt)
            
            
            json_data = {

                "qcl_generic_data": {
                    "qcl_source_id": buyerId,
                    "qcl_destination_id": sellerId
                },
                "qcl_transaction_data": {
                    "generic_fields": {},
                    "source_fields": {
                        "from_date": parsed_orderdate_gt,
                        "to_date": parsed_orderdate_lt,
                        "offset": offset,
                        "limit": limit
                    },
                    "destination_fields": {}
            }
                }
            
        return True, 200, json_data, None, None, None, None

                
    except Exception as e: 
        statusCode = 500
        message =  str(e)
        reason = "Invalid value"
        reference_error = None
        messageCode = "internalError"
        PropertyPath = None
        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
    
def map_orders_list_fields(request_data):
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
        
        field_json = field_mapping_key_val.get("qcl_cc_order")
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
                            qcl_generic_field_key: transaction_data.get("genericFields", {}),
                            qcl_dest_field_key: transaction_data.get("destinationFields", {}),
                            qcl_src_field_key: transaction_data.get("sourceFields", {})
                        }
                    })
                                
            return True, 200, qcl_request_dict, None, None, None, None
    
    except Exception as e:
        
        statusCode = 500
        message =  str(e)
        reason = "Invalid value"
        reference_error = None
        messageCode = "internalError"
        PropertyPath = None
        return False, statusCode, message, reason, reference_error, messageCode, PropertyPath
