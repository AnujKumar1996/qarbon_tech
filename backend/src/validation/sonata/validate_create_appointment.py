from datetime import datetime, timezone


from src.validation.sonata.validate_create_order import (
    validate_product_order_item_notes,
     validate_related_contact_information)



def  validate_user_startdatetime(buyer_startdatetime):
   """
    Validates the buyer's start date and time.

    Parameters:
    - buyer_startDateTime (str): The start date and time provided by the buyer in the format '%Y-%m-%dT%H:%M:%S.%fZ'.

    Returns:
    - bool: True if the provided start date and time is after the current UTC time; False otherwise.
    """
  
   current_time = datetime.utcnow()
   formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
   
   if buyer_startdatetime <= formatted_time :
      return False
   return True

def validate_user_enddatetime(buyer_startdatetime,buyer_enddatetime)  :
   
   """
    Validates the buyer's end date and time relative to the start date and time.

    Parameters:
    - buyer_startDateTime (str): The start date and time provided by the buyer in the format '%Y-%m-%dT%H:%M:%S.%fZ'.
    - buyer_endDateTime (str): The end date and time provided by the buyer in the format '%Y-%m-%dT%H:%M:%S.%fZ'.

    Returns:
    - bool
   """
   
   if buyer_startdatetime > buyer_enddatetime :
         return False
      
   return True


def validate_create_appointment(order_data, response_data):
    """
    Validating appointment response
    """
    # checking note
    if 'note' in order_data:
      order_notes = order_data.get("note")
      response_notes = response_data.get("note")
      if order_notes is not None:
        if not validate_product_order_item_notes(order_notes, response_notes):
          return False 
        
    # checking relatedContactInformation
    order_related_contact_information = order_data.get('relatedContactInformation')
    response_related_contact_information = response_data.get('relatedContactInformation')
    if not validate_related_contact_information(order_related_contact_information, response_related_contact_information):
        return False
    
    # checking workOrder
    if order_data.get("workOrder") != response_data.get("workOrder"):
       return False
    
    # checking attachment
    user_atteachment=order_data.get("attachment") 
    json_attechment=response_data.get("attachment")

    if user_atteachment is not None and json_attechment is not None :
       
      user_excluded_order_product = [{key: value for key, value in user_attachment_item.items() if key != 'creationDate'}for user_attachment_item in order_data.get("attachment") ]
      json_excluded_order_product = [{key: value for key, value in json_attachment_item.items() if key != 'creationDate'}for json_attachment_item in response_data.get("attachment") ]
   
      if user_excluded_order_product != json_excluded_order_product:
         
         return False  
    
    return True, None  


def convert_to_utc_iso_range(buyer_startdatetime, buyer_enddatetime):
    """
    Converts a range of datetime strings to a specified ISO 8601 format in UTC.

    Args:
        buyer_startdatetime: The start datetime string in the original format.
        buyer_enddatetime: The end datetime string in the original format.
        input_format: The format of the input datetime strings. Default is "%Y-%m-%d %H:%M:%S.%f%z".
        output_format: The desired output format. Default is "%Y-%m-%dT%H:%M:%S.%fZ".

    Returns:
        Tuple containing converted start and end datetime strings in the desired format.
    """
    
    input_format="%Y-%m-%d %H:%M:%S.%f%z"
    output_format="%Y-%m-%dT%H:%M:%S.%fZ"
    start_datetime = datetime.strptime(str(buyer_startdatetime), input_format)
    end_datetime = datetime.strptime(str(buyer_enddatetime), input_format)

  
    converted_startdatetime = start_datetime.astimezone(timezone.utc).strftime(output_format)
    converted_enddatetime = end_datetime.astimezone(timezone.utc).strftime(output_format)

    return converted_startdatetime, converted_enddatetime


def checking_relatedcontactinfo(order_data, appointment_json_data_of_particular_id):
    """
    Validating user relatedContactInformation with appointment relatedContactInformation
    """
    
    order_related_contact_information = order_data.get('relatedContactInformation')
    response_related_contact_information = appointment_json_data_of_particular_id.get('relatedContactInformation')
    if not validate_related_contact_information(order_related_contact_information, response_related_contact_information):
        return False

    return True


def  validate_lesser_than_current_datetime(buyer_startdatetime):
   
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    if buyer_startdatetime >= formatted_time :
        return False
    return True