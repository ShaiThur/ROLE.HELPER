from typing import Optional

from fastapi import APIRouter, UploadFile, File
from starlette import status

from dto import SystemResponse
from service.voice_transcription import transcribe

voice_router = APIRouter(prefix="/voice", tags=["voice"])


@voice_router.post(
    "/transcribe",
    response_model=SystemResponse,
    responses={
        status.HTTP_200_OK:
            {
                "model": SystemResponse,
                "description": "The service has successfully processed the request"
            }
    }
)
async def transcribe_text(
        file_to_process: Optional[UploadFile | str] = File(None)
) -> SystemResponse:
    return await transcribe(file_to_process)
