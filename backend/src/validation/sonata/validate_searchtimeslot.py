from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder
from src.schemas.interlude_schemas.error_schemas import Error422
from fastapi.responses import JSONResponse
from fastapi import status


def validate_searchtimeslot(order_data, response_data):
    """
    Validating searchTimeSlot response
    """
    if order_data.get("workOrder") != response_data.get("workOrder"):
       return False
    
    return True


def validate_startDateTime(response_data):
    
    """
    Validating Response startDateTime with current datatime
    """

    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    seller_availableTimeSlot=response_data.get('availableTimeSlot')
    for item in seller_availableTimeSlot:
      validFor=item.get('validFor')  
      startDateTime=validFor.get("startDateTime")
      
     
      if startDateTime < formatted_time :
         return False
    return True  

def validate_endDateTime(response_data):
    
    """
    Validating Response endDateTime with startDateTime
    """
   
    seller_availableTimeSlot=response_data.get('availableTimeSlot')
    
    for item in seller_availableTimeSlot:
      validFor=item.get('validFor')  
      endDateTime=validFor.get("endDateTime") 
      startDateTime=validFor.get("startDateTime")
      
      if endDateTime < startDateTime  :
        return False
      
    return True
       
    

def validate_user_startDateTime(order_data):
    """
    Validating Request startDateTime with current datetime
    """

    buyer_requestedTimeSlot = order_data.get('requestedTimeSlot')
    
    for item in buyer_requestedTimeSlot:
        
        validFor = item.get('validFor')  
        startDateTime = validFor.get("startDateTime")

        # Get the current UTC time as an offset-aware datetime object
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        # Convert startDateTime and endDateTime to offset-aware datetime objects
        startDateTime = startDateTime.replace(tzinfo=timezone.utc)

        if startDateTime < current_time :
            return False
    return True





def validate_user_endDateTime(order_data):
    """
    Validating Request endDateTime with Request startDateTime
    """
    
    buyer_requestedTimeSlot = order_data.get('requestedTimeSlot')
    
    for item in buyer_requestedTimeSlot:
        validFor = item.get('validFor')  
        endDateTime = validFor.get("endDateTime") 
        startDateTime = validFor.get("startDateTime")
        
        if endDateTime < startDateTime :
            return False
      
    return True


