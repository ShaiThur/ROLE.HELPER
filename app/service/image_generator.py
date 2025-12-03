import json
import logging

import httpx
from httpx import Response

from common import ModelsConstants
from common.enums import ImageTheme
from common.prompts import IMAGE_LOCATION_GENERATION_PROMPT, IMAGE_PERSON_GENERATION_PROMPT
from dto.image import ImageResponse

log = logging.getLogger(__name__)


async def __prepare_prompt__(context: str) -> ImageTheme:
    response = await ModelsConstants.GROQ_CLIENT.chat.completions.create(
        model=ModelsConstants.LLM_STRUCTURED_OUTPUT_NAME,
        messages=[
            {
                "role": "system",
                "content": IMAGE_LOCATION_GENERATION_PROMPT,
            },
            {
                "role": "user",
                "content": context
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "intent_classification",
                "schema": ImageResponse.model_json_schema()
            }
        }
    )

    raw_result = json.loads(response.choices[0].message.content or "{}")
    result = ImageResponse.model_validate(raw_result)
    if result.theme is ImageTheme.USER:
        return IMAGE_PERSON_GENERATION_PROMPT.format(context=context)
    else:
        return IMAGE_LOCATION_GENERATION_PROMPT.format(context=context)


async def __create_image_prompt__(context: str) -> str:
    response = await ModelsConstants.GROQ_CLIENT.chat.completions.create(
        model=ModelsConstants.LLM_NAME,
        messages=[{"role": "system", "content": context}],
        temperature=0.75,
        max_completion_tokens=1024,
        top_p=0.95,
        reasoning_effort="none",
        stop=None
    )
    return response.choices[0].message.content


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


async def create_image(context: str) -> Response:
    prepared_prompt = await __prepare_prompt__(context)
    image_prompt = await __create_image_prompt__(prepared_prompt)
    return await __create_image__(image_prompt)
