from datetime import datetime
from typing import Optional, List, Sequence

from sqlalchemy import select, delete

from common import connection_manager
from dto import UserRequest
from models import UserSessionHistory


async def create_user_session(
        user_request: UserRequest,
        answer: str,
        answer_embedding: Optional[List[float]] = None,
        is_description: bool = False
) -> UserSessionHistory:
    async with connection_manager.get_connection_async() as session:
        record = UserSessionHistory(
            session_id=user_request.session_id,
            user_id=user_request.user_id,
            query=user_request.input_text,
            answer=answer,
            answer_embedding=answer_embedding,
            creation_date=datetime.now(),
            is_description=is_description
        )
        session.add(record)
        await session.flush()
        await session.refresh(record)
        return record

async def get_by_user_and_session_id(
        user_id: str,
        session_id: str,
        order_by_date: bool = True
) -> Sequence[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(UserSessionHistory).where(
            (UserSessionHistory.session_id == session_id) &
            (UserSessionHistory.user_id == user_id)
        )
        if order_by_date:
            stmt = stmt.order_by(UserSessionHistory.creation_date.asc())

        result = await session.execute(stmt)
        return result.scalars().all()

async def update_user_session(
        user_id: str,
        session_id: str,
        **kwargs
) -> Optional[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(UserSessionHistory).where(
            (UserSessionHistory.user_id == user_id) &
            (UserSessionHistory.session_id == session_id)
        )
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record:
            for key, value in kwargs.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            await session.flush()
            await session.refresh(record)

        return record

async def delete_by_session_id(
        user_id: str,
        session_id: str
) -> int:
    async with connection_manager.get_connection_async() as session:
        stmt = delete(UserSessionHistory).where(
            (UserSessionHistory.user_id == user_id) &
            (UserSessionHistory.session_id == session_id)
        )
        result = await session.execute(stmt)
        return result.rowcount

async def search_similar(
        embedding: List[float],
        limit: int = 10
) -> Sequence[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = (
            select(UserSessionHistory)
            .where(UserSessionHistory.answer_embedding.isnot(None))
            .order_by(UserSessionHistory.answer_embedding.cosine_distance(embedding))
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
