from pydantic import BaseModel, Field

from common.enums import Intent


class IntentResponse(BaseModel):
    intent: Intent = Field(Intent.OTHER, description="намерение пользователя")
