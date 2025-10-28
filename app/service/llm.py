import logging
from typing import Optional

from fastapi import UploadFile
import json

from common import ModelsConstants, INTENT_PROMPT
from common.enums import Intent
from dto import UserRequest, SystemResponse, IntentResponse
from dto.routing import AskFormat
from repository.session import create_session
from service.voice_transcription import transcribe
from repository.user_session_history import create_user_session

log = logging.getLogger(__name__)


async def define_intent(user_query: str) -> Intent:
    response = await ModelsConstants.GROQ_CLIENT.chat.completions.create(
        model=ModelsConstants.LLM_STRUCTURED_OUTPUT_NAME,
        messages=[
            {
                "role": "system",
                "content": INTENT_PROMPT,
            },
            {
                "role": "user",
                "content": user_query
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "intent_classification",
                "schema": IntentResponse.model_json_schema()
            }
        }
    )

    raw_result = json.loads(response.choices[0].message.content or "{}")
    result = IntentResponse.model_validate(raw_result)
    return result.intent


async def name_the_session(user_query: str, session_id: str) -> None:
    pass


async def run_processing(user_query: UserRequest, file: Optional[UploadFile | str] = None) -> SystemResponse:
    if user_query.ask_format == AskFormat.VOICE:
        user_query.input_text = (await transcribe(file)).text
        log.debug(f"transcribed {user_query.input_text}")

    intent = await define_intent(user_query.input_text)
    session_id = (await create_session(user_query.session_id, user_query.user_id)).id
    await create_user_session(user_query.input_text, session_id, intent)

    match intent:
        case Intent.OTHER:
            return SystemResponse(session_id=session_id, text="Не совсем понял, задай вопрос еще раз, пожалуйста")
        case _:
            return SystemResponse(session_id=session_id, text=intent)
