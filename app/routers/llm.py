from typing import Optional

from fastapi import APIRouter, UploadFile, File
from starlette import status

from dto import SystemResponse, UserRequest
from service.llm import run_processing

llm_router = APIRouter(prefix="/llm", tags=["main controller"])


@llm_router.post(
    "/ask",
    response_model=SystemResponse,
    responses={
        status.HTTP_200_OK:
            {
                "model": SystemResponse,
                "description": "The service has successfully processed the request"
            }
    }
)
async def ask_llm(
        request: UserRequest,
        file_to_process: Optional[UploadFile | str] = File(None)
) -> SystemResponse:
    return await run_processing(request, file_to_process)
