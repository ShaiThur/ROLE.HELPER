from pydantic import BaseModel

from common.enums import ImageTheme


class CreateImageRequest(BaseModel):
    session_id: str
    theme: ImageTheme
