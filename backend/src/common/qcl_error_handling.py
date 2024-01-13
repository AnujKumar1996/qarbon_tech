from src.common.exceptions import raise_exception
from starlette.responses import JSONResponse 
from src.common.extract_error_message import extract_error_msg
from src.call_external_apis.call_qcl_renew_token_api import call_qcl_renew_token_api



def handle_qcl_error(qcl_response, refresh_token, mapped_data, function_to_call):
    if qcl_response.status_code not in (200, 201, 413, 415): error_msg = extract_error_msg(qcl_response)
    
    if isinstance(qcl_response, str):
        return raise_exception(404, "sonata_payloads.json or properties.json file not found", "Not found", None, "notFound", None)
            
    if qcl_response.status_code == 422:
        status_msg_code = 422
        message = error_msg
        reason = qcl_response.reason
        reference_error = None
        message_code = "otherIssue"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    elif qcl_response.status_code == 400:
        status_msg_code = 400
        message = error_msg
        reason = qcl_response.reason
        reference_error = None
        message_code = "invalidBody"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    elif qcl_response.status_code == 413:
        status_msg_code = 413
        message = qcl_response.text
        reason = qcl_response.reason
        reference_error = None
        message_code = "tooLarge"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    elif qcl_response.status_code == 415:
        status_msg_code = 415
        message = qcl_response.text
        reason = qcl_response.reason
        reference_error = None
        message_code = "unsupportedMediaType"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    elif qcl_response.status_code == 401:
        response_data = call_qcl_renew_token_api(refresh_token)
        
        if isinstance(response_data,JSONResponse):
            return response_data
    
        response_data = response_data.json().get("data").get("data")
        access_token = response_data.get("AccessToken")
        token_type = response_data.get("TokenType")
        
        new_qcl_response = function_to_call(mapped_data, access_token, refresh_token, token_type)
        
        if new_qcl_response.status_code == 401:    
            status_msg_code = 401
            message = "Unauthorized"
            reason = qcl_response.reason
            reference_error = None
            message_code = "invalidCredentials"
            property_path = None
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
        else:
            return new_qcl_response
        
    elif qcl_response.status_code == 403:
        status_msg_code = 403
        message = error_msg
        reason = qcl_response.reason
        reference_error = None
        message_code = "forbiddenRequester"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    
    elif qcl_response.status_code == 404:
        status_msg_code = 404
        message = "Attachment Id not found"
        reason = "Attachment not found"
        reference_error = None
        message_code = "notFound"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)
    

    elif qcl_response.status_code == 500:
        status_msg_code = 500
        message = error_msg
        reason = qcl_response.reason
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    else:
        return qcl_response