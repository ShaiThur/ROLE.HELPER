from typing import List

from fastapi import APIRouter, Query

from dto.routing import HistoryResponse
from service.user_session import get_user_history

history_router = APIRouter(prefix="/history", tags=["history"])


@history_router.get("/user_history")
async def get_history(
        user_id: str = Query(...),
        session_id: str = Query(...),
) -> List[HistoryResponse]:
    return await get_user_history(user_id, session_id)