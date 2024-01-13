import json
from pathlib import Path
from src.common.exceptions import raise_exception
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.common.create_jsonfile import create_response_json
from src.schemas.sonata_schemas.common_schemas import ProductOrder
from src.validation.sonata.validate_modify_order import validate_modify_order


def modify_product_order(order):
    """
    This operation modifies a ProductOrder entity.
    """
    
    order = order.model_dump(
        by_alias=True
    )

    cwd = Path(__file__).parents[1]
    file_name = cwd / 'responses' / 'sonata_response.json'
    
    if not file_name.exists() :
            status_msg_code = 404
            message = f"File not found '{file_name}'"
            reason = "File not found"
            reference_error = None
            message_code = "notFound"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)

    try:
        with open(file_name, "r") as json_file:
            json_data = json.load(json_file)
    except json.JSONDecodeError as e:
            
            status_msg_code = 422
            message = "Record not found"
            reason = "Record not found"
            reference_error = None
            message_code = "invalidValue"
            property_path =None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

    
    user_data_productorderitem = order.get("productOrderItem")

    is_item_present = False
    product_order_id = None
   
    for user_data in user_data_productorderitem:
       
        for product_order_id, existing_json_data in json_data.items():
           
            for json_data_item in existing_json_data.get("productOrderItem"):

                if json_data_item.get("id")== user_data.get("id"):
                    
                    if user_data.get("action") != "modify":
                        
                        status_msg_code = 422
                        message ="'action' should be 'modify'"
                        reason = "Invalid action value"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path =None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                
                    if "requestedItemTerm" in user_data and user_data.get('requestedItemTerm') is None:
                        
                        status_msg_code = 422
                        message ="Buyer must provide the requestedItemTerm when 'action' is 'modify'"
                        reason = "'requestedItemTerm' is missing"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path =None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                    if "product" in user_data and "id" in user_data.get('product'):
                        if json_data_item.get('product') is None:
                            if 'place' not in user_data.get('product') and 'productRelationship' not in user_data.get('product') and 'productOffering' not in user_data.get('product'):
                                pass
                            else:
                                
                                status_msg_code = 422
                                message ="Modifying productOffering, productRelationship and place is not allowed"
                                reason = reason = "Mismatched values in productOffering, productRelationship and place during modify request"
                                reference_error = None
                                message_code = "invalidValue"
                                property_path =None
                                
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                        else:

                            if 'productConfiguration' not in user_data.get('product'):
                                
                                status_msg_code = 422
                                message = "The Buyer must provide productConfiguration"
                                reason = "Missing productConfiguration in modify request"
                                reference_error = None
                                message_code = "invalidValue"
                                property_path =None
                                
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                        
                            if user_data.get('product', {}).get("productRelationship") != json_data_item.get('product', {}).get('productRelationship'):

                                
                                status_msg_code = 422
                                message = "Modifying productRelationship is not allowed."
                                reason = "Mismatched 'productRelationship' in modify request"
                                reference_error = None
                                message_code = "invalidValue"
                                property_path =None
                                
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                            
                            if (user_data.get('product', {}).get('productOffering') and
                                    user_data['product']['productOffering'] != json_data_item.get('product', {}).get('productOffering')
                                ):
                                
                                status_msg_code = 422
                                message = "Modifying 'productOffering' is not allowed."
                                reason = "Mismatched 'productOffering' in modify request"
                                reference_error = None
                                message_code = "invalidValue"
                                property_path =None
                                
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                            user_data_productPlace = user_data.get('product').get('place')
                            json_productPlace = json_data_item.get('product').get('place')
                            
                            if (user_data_productPlace is not None and json_productPlace is None) or (user_data_productPlace is None and json_productPlace is not None):
                               
                                status_msg_code = 422
                                message = "Modifying 'product's place' is not allowed."
                                reason = "Mismatched 'place' in modify request"
                                reference_error = None
                                message_code = "invalidValue"
                                property_path = None
                                
                                return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                            
                            elif user_data_productPlace is None and json_productPlace is None:
                                pass

                            else:
                                for user_data_item in user_data_productPlace:
                                    user_data_schemaLocation = user_data_item.get('@schemaLocation')
                                    user_data_sch_string = str(user_data_schemaLocation)
                                    user_data_type = user_data_item.get('@type')
                                    user_data_role = user_data_item.get('role')
                                    for json_data_place in json_productPlace:
                                        json_data_schemaLocation = json_data_place.get('@schemaLocation')
                                        json_data_type = json_data_place.get('@type')
                                        json_data_role = json_data_place.get('role')
                                        
                                        if (user_data_sch_string != json_data_schemaLocation or user_data_type != json_data_type or  user_data_role != json_data_role):
                                            
                                            status_msg_code = 422
                                            message =  "Modifying 'product's place' is not allowed."
                                            reason = "Mismatched 'place' in modify request"
                                            reference_error = None
                                            message_code = "invalidValue"
                                            property_path = None
                                            
                                            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    

                        json_data_item['action'] = user_data.get("action")
                        json_data_item['product']['id'] = user_data.get('product', {}).get('id')
                        json_data_item['product']['productConfiguration'] = user_data.get('product', {}).get('productConfiguration')
                        is_item_present = True
                        
                        
                    else:
                        
                        status_msg_code = 422
                        message = "product can not be null and product Identifier must be provided"
                        reason = "Id not found"
                        reference_error = None
                        message_code = "invalidValue"
                        property_path = None
                        
                        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)    
                
    if is_item_present:
       
        response_data = jsonable_encoder(ProductOrder(**existing_json_data))
        is_validated = validate_modify_order(order, response_data)
        if not is_validated:
            status_msg_code = 422
            message = "Request and Response data mismatch."
            reason = "Validation error"
            reference_error = None
            message_code = "invalidValue"
            property_path = None
            
            return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)


        else:

            create_response_json(product_order_id, response_data, file_name)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response_data,
                media_type="application/json;charset=utf-8"
            )
        
    else:
        
        status_msg_code = 422
        message = "ProductOrderItem Identifier not found"
        reason = "Id not found"
        reference_error = None
        message_code = "invalidValue"
        property_path = None
        
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path)