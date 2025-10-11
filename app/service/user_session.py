from typing import List

from dto.routing import HistoryResponse
from repository.user_session import get_by_user_and_session_id


async def get_user_history(
        user_id: str,
        session_id: str,
) -> List[HistoryResponse]:
    records = await get_by_user_and_session_id(user_id, session_id)
    return [
        HistoryResponse(
            query=r.query,
            answer=r.answer,
            timestamp=r.creation_date
        ) for r in records
    ]
