from fastapi import BackgroundTasks, APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from src.order_status_utils.periodic_api_call import periodic_api_call
from src.order_status_utils.set_env_file import set_env_file
from src.common.exceptions import raise_exception

router = APIRouter(
    prefix="/mef/v1/accounting/transaction",
    tags=["QCL Transaction API"]
)

token = HTTPBearer()

@router.get("/status")
async def fetch_lattice_transaction_id_status(
    background_tasks: BackgroundTasks,
    header_request:Request,
    header_token: str = Depends(token)
    ):
    """
    Start the periodic task in the background.
    """
    refresh_token = header_request.headers.get("Refreshtoken")
    access_token = header_token.credentials

    set_env_file(AccessToken = access_token, RefreshToken = refresh_token)
    background_tasks.add_task(periodic_api_call)
    return {"message": "Periodic task started"}
