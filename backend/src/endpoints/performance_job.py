from typing import Union
from fastapi import (APIRouter,Response,status)
from fastapi.security import HTTPBearer
from src.common.exceptions import raise_exception
from src.schemas.interlude_schemas.common_schemas import \
    PerformanceJob_Create
from src.schemas.interlude_schemas.performance_job_schemas import PerformanceJob
from src.common.json_read import common_schema
from .response_headers import add_headers
from src.schemas.interlude_schemas.error_schemas import (Error400, Error401,
                                                         Error403, Error422,
                                                         Error500,Error408)
from src.performance_job_operations.create_performance_job import create_performance_job


security = HTTPBearer()

router = APIRouter(
    prefix="/v1/MEF/lsoInterlude/performanceMonitoring"
)


@router.post("/performanceJob",tags=["performanceJob"], status_code=status.HTTP_201_CREATED,response_model=
            Union[PerformanceJob,Error422, Error500, Error400, Error403, Error401,Error408],
    responses={
        201: common_schema["performance_job_201"],
        400: common_schema["response_400"],
        401: common_schema["response_401"],
        403: common_schema["response_403"],
        500: common_schema["response_500"],
        422: common_schema["response_422"],
    },
)
async def creates_a_performance_job(jobdata:PerformanceJob_Create, response: Response):
    '''
    A request initiated by the Buyer/Client to create a Performance Job in the Seller/Server system to indicate performance monitoring objectives.
    '''
    add_headers(response)
    try:
        order_dict = jobdata.model_dump(by_alias=True)
        return create_performance_job(order_dict)
        
    except Exception as err:
        status_msg_code = 500
        message = str(err)
        reason = "The server encountered an unexpected condition that prevented it from fulfilling the request"
        reference_error = None
        message_code = "internalError"
        property_path = None
        return raise_exception(status_msg_code, message, reason, reference_error, message_code, property_path) 
