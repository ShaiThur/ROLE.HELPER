import logging
import uuid

from fastapi import UploadFile

from common import ModelsConstants, FileToProcessError
from dto import SystemResponse


async def transcribe(file: UploadFile | str) -> SystemResponse:
    if (isinstance(file, str)
            or file.content_type not in ["audio/mp3", "audio/wav", "audio/ogg", "audio/mpeg"]
            or file.size > ModelsConstants.FILE_SIZE_LIMIT_IN_MB):
        raise FileToProcessError("File cannot be processed")

    with file.file as file_data:
        transcription = await ModelsConstants.GROQ_CLIENT.audio.transcriptions.create(
            file=(f"{uuid.uuid4()}.mp3", file_data.read()),
            model=ModelsConstants.ASR_NAME,
            language="ru",
            response_format="text",
        )
        logging.info("Transcription complete: %s", transcription)
        return SystemResponse(text=transcription)
