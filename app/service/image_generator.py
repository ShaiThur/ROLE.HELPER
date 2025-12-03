import logging

import httpx
from httpx import Response

from common import ModelsConstants
from common.enums import ImageTheme
from common.prompts import IMAGE_GENERATION_PROMPT
from service.llm import send_base_llm_response
from service.user_session import get_user_history

log = logging.getLogger(__name__)


async def __prepare_prompt__(text: str, theme: ImageTheme) -> str:
    theme_text = ImageTheme.value_of(theme)
    prompt = IMAGE_GENERATION_PROMPT.format(theme=theme_text, info=text)
    return await send_base_llm_response(
        [
            {"role": "system", "content": prompt}
        ]
    )


async def __create_image__(prompt: str):
    input = {
        "prompt": prompt,
        "height": 1024,
        "width": 1024,
        "num_steps": 10
    }
    headers = {
        'Authorization': f'Bearer {ModelsConstants.API_IMAGE_KEY}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(ModelsConstants.IMAGE_GENERATION_NAME, headers=headers, json=input)
        return response


async def create_image(session_id: str, theme: ImageTheme) -> Response:
    history_responses = await get_user_history(session_id)
    text = [
        i.answer for i in history_responses
        if "Эпоха" in i.answer and theme == ImageTheme.THEME
           or "Предыстория" in i.answer and theme == ImageTheme.USER
    ][0]
    prompt = await __prepare_prompt__(text, theme)
    return await __create_image__(prompt)
