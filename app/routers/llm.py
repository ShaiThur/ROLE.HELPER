from typing import Optional

from fastapi import APIRouter, UploadFile, File, Cookie, Query
from starlette import status

from dto import SystemResponse, UserRequest
from service.llm import run_processing, summarize_info

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
        user_id: str = Cookie(""),
    file_to_process: Optional[UploadFile | str] = File(None)
) -> SystemResponse:
    if user_id != "":
        request.user_id = user_id
    return await run_processing(request, file_to_process)


@llm_router.get(
    "/summarize",
    response_model=SystemResponse,
    responses={
        status.HTTP_200_OK:
            {
                "model": SystemResponse,
                "description": "The service has successfully processed the request"
            }
    }
)
async def summarize_session(
        session_id: str = Query()
) -> SystemResponse:
    summary = await summarize_info(session_id)
    return SystemResponse(
        session_id=session_id,
        text=summary
    )
