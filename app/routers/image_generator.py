import os
import uuid
from io import BytesIO

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from dto.image import CreateImageRequest, CreateImageResponse
from service.image_generator import create_image

image_router = APIRouter(prefix="", tags=["image"])


@image_router.post("/image")
async def create_image_by_theme(request: CreateImageRequest) -> CreateImageResponse:
    data = (await create_image(request.context))

    if not os.path.exists("../images"):
        os.makedirs("../images")

    image_id = uuid.uuid4()

    with open(f"../images/{image_id}.png", "wb") as f:
        f.write(data.content)

    return CreateImageResponse(
        img_id=str(image_id),
        img_path=f"./app/images/{image_id}.png"
    )


@image_router.get("/image/{img_id}")
async def get_image_by_img_id(img_id: str) -> CreateImageResponse:
    print(os.path.exists(f"../images/{img_id}.png"))
    if os.path.exists(f"../images/{img_id}.png"):
        return CreateImageResponse(
            img_id=img_id,
            img_path=f"./app/images/{img_id}.png"
        )
    else:
        raise ValueError()


@image_router.get("/image/show/{img_id}")
async def show_image_by_img_id(img_id: str) -> StreamingResponse:
    print(os.path.exists(f"../images/{img_id}.png"))
    if os.path.exists(f"../images/{img_id}.png"):
        with open(f"../images/{img_id}.png", "rb") as f:
            return StreamingResponse(BytesIO(f.read()), media_type="image/png")
    else:
        raise ValueError()
