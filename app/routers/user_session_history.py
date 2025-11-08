from typing import List, Dict

from fastapi import APIRouter, Query, Cookie

from dto import SessionRequest
from dto.routing import HistoryResponse, SessionResponse
from service.user_session import get_user_history, get_user_sessions, change_session_name

history_router = APIRouter(prefix="/history", tags=["history"])


@history_router.get("/user_history")
async def get_history(
        session_id: str = Query(),
) -> List[HistoryResponse]:
    return await get_user_history(session_id)


@history_router.get("/user_sessions")
async def get_sessions(
        user_id: str = Cookie(),
) -> List[SessionResponse]:
    return await get_user_sessions(user_id)


@history_router.patch("/change_name")
async def change_name(session_request: SessionRequest) -> Dict[str, str]:
    await change_session_name(session_request)
    return {"result": "success"}
