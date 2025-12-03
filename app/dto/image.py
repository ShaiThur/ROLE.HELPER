from pydantic import BaseModel, Field

from common.enums import ImageTheme


class ImageResponse(BaseModel):
    theme: ImageTheme = Field(description="тема запроса")


class CreateImageRequest(BaseModel):
    context: str


class CreateImageResponse(BaseModel):
    img_id: str
    img_path: str
