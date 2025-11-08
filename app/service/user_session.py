from typing import List, Optional

from dto import SessionRequest
from dto.routing import HistoryResponse, SessionResponse
from repository.session import get_sessions_by_user_id, change_session_description
from repository.user_session_history import get_by_session_id


async def get_user_history(
        session_id: str,
) -> List[HistoryResponse]:
    records = await get_by_session_id(session_id)
    return [
        HistoryResponse(
            query=r.query,
            answer=r.answer,
            timestamp=r.creation_date
        ) for r in records
    ]


async def get_user_sessions(user_id: str) -> List[SessionResponse]:
    return [
        SessionResponse(session_id=s.id, session_name=s.description)
        for s in await get_sessions_by_user_id(user_id)
    ]


async def change_session_name(session_request: SessionRequest):
    await change_session_description(session_request.session_id, session_request.text)
