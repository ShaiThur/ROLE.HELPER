import json
import logging
from typing import Optional, List, Dict

from fastapi import UploadFile

from common import ModelsConstants, INTENT_PROMPT, INTENT_SUBPROMPT, SETTING_PROMPT, CommonConstants, \
    CREATE_USER_PROMPT, CREATE_USER_SUBPROMPT
from common.enums import Intent
from dto import UserRequest, SystemResponse, IntentResponse, HistoryResponse
from dto.routing import AskFormat
from repository.session import create_session
from repository.user_session_history import create_user_session
from service.user_session import get_user_history
from service.voice_transcription import transcribe

log = logging.getLogger(__name__)


async def send_base_llm_response(messages: List[Dict[str, str]]) -> str:
    response = await ModelsConstants.GROQ_CLIENT.chat.completions.create(
        model=ModelsConstants.LLM_NAME,
        messages=messages,
        temperature=0.75,
        max_completion_tokens=1024,
        top_p=0.95,
        reasoning_effort="none",
        stop=None
    )

    return response.choices[0].message.content


async def define_intent(user_query: str, context: Optional[HistoryResponse]) -> Intent:
    if context:
        sub_prompt = INTENT_SUBPROMPT.format(user=context.query, assistant=context.answer)
    else:
        sub_prompt = ""
    response = await ModelsConstants.GROQ_CLIENT.chat.completions.create(
        model=ModelsConstants.LLM_STRUCTURED_OUTPUT_NAME,
        messages=[
            {
                "role": "system",
                "content": INTENT_PROMPT.format(sub_prompt),
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


async def create_scenario(user_query: str, context: Optional[List[HistoryResponse]]) -> str:
    messages = [
        {
            "role": "system",
            "content": SETTING_PROMPT,
        },
    ]
    user_prevs =[
        [
            {
                "role": "user",
                "content": c.query,
            },
            {
                "role": "assistant",
                "content": c.answer,
            }
        ] for c in context[0:len(context) if 5 >= len(context) > 0 else 0 if len(context) == 0 else 5]
    ]
    log.info(f"Previous messages: {user_prevs}")

    for prev in user_prevs:
        messages.extend(prev)

    messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )
    return await send_base_llm_response(messages)


async def create_user_specs(user_query: str, context: Optional[List[HistoryResponse]]) -> str:
    if len(context) > 0:
        sub_prompt = CREATE_USER_SUBPROMPT.format(context[-1].answer)
    else:
        sub_prompt = ""

    messages = [
        {
            "role": "system",
            "content": CREATE_USER_PROMPT.format(sub_prompt),
        },
    ]
    user_prevs = [
        [
            {
                "role": "user",
                "content": c.query,
            },
            {
                "role": "assistant",
                "content": c.answer,
            }
        ] for c in context[0:len(context) if 5 >= len(context) > 0 else 0 if len(context) == 0 else 5]
    ]
    log.info(f"Previous messages: {user_prevs}")

    for prev in user_prevs:
        messages.extend(prev)

    messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )
    return await send_base_llm_response(messages)


async def run_processing(user_query: UserRequest, file: Optional[UploadFile | str] = None) -> SystemResponse:
    if user_query.ask_format == AskFormat.VOICE:
        user_query.input_text = (await transcribe(file)).text
        log.debug(f"transcribed {user_query.input_text}")

    session_id = (await create_session(user_query.session_id, user_query.user_id)).id
    messages = await get_user_history(session_id)
    log.info(f"Messages: {messages}")
    intent = await define_intent(user_query.input_text, messages[-1] if messages else None)
    log.info(f"Intent: {intent}")

    match intent:
        case Intent.OTHER:
            await create_user_session(user_query.input_text, session_id, CommonConstants.DEFAULT_REJECTION, Intent.OTHER.name)
            return SystemResponse(session_id=session_id, text=CommonConstants.DEFAULT_REJECTION)
        case Intent.NEW_SCENARIO:
            scenario_response = await create_scenario(user_query.input_text, messages)
            await create_user_session(user_query.input_text, session_id, scenario_response, Intent.NEW_SCENARIO)
            return SystemResponse(session_id=session_id, text=scenario_response)
        case Intent.CREATE_USER:
            user_response = await create_user_specs(user_query.input_text, messages)
            await create_user_session(user_query.input_text, session_id, user_response, Intent.CREATE_USER)
            return SystemResponse(session_id=session_id, text=user_response)
        case _:
            return SystemResponse(session_id=session_id, text=intent)
