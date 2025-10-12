import json
from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, model_validator


class AskFormat(StrEnum):
    TEXT = "TEXT"
    VOICE = "VOICE"


class UserRequest(BaseModel):
    user_id: str
    session_id: str
    ask_format: AskFormat = AskFormat.TEXT
    input_text: Optional[str] = "Скажи привет"

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class SystemResponse(BaseModel):
    text: str


class HistoryResponse(BaseModel):
    query: str
    answer: str
    timestamp: datetime
