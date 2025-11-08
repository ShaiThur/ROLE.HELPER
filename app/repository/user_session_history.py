from datetime import datetime
from typing import Optional, List, Sequence

from sqlalchemy import func
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from common import connection_manager
from models import UserSessionHistory
from models.user_session_history import Session


async def create_user_session(
        input_text: str,
        session_id: str,
        answer: str,
        intent: str,
        answer_embedding: Optional[List[float]] = None,
        is_description: bool = False
) -> UserSessionHistory:
    async with connection_manager.get_connection_async() as session:
        record = UserSessionHistory(
            session_id=session_id,
            query=input_text,
            answer=answer,
            answer_embedding=answer_embedding,
            creation_date=datetime.now(),
            is_description=is_description,
            intent=intent
        )
        session.add(record)
        await session.flush()
        await session.refresh(record)
        return record


async def get_by_session_id(
        session_id: str,
        order_by_date: bool = True
) -> Sequence[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(UserSessionHistory).where(
            UserSessionHistory.session_id == session_id
        )
        if order_by_date:
            stmt = stmt.order_by(UserSessionHistory.creation_date.desc())

        result = await session.execute(stmt)
        return result.scalars().all()


async def get_sessions_by_user_id(
        user_id: str,
        limit: int = 100,
        offset: int = 0
) -> Sequence[Session]:
    async with connection_manager.get_connection_async() as session:
        stmt = (
            select(Session)
            .where(Session.user_id == user_id)
            .options(selectinload(Session.user_sessions))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_session_with_history(session_id: str) -> Optional[Session]:
    async with connection_manager.get_connection_async() as session:
        stmt = (
            select(Session)
            .where(Session.id == session_id)
            .options(selectinload(Session.user_sessions))
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def update_user_session(
        record_id: int,
        **kwargs
) -> Optional[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(UserSessionHistory).where(
            UserSessionHistory.id == record_id
        )
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record:
            for key, value in kwargs.items():
                if hasattr(record, key) and key != 'id':
                    setattr(record, key, value)
            await session.flush()
            await session.refresh(record)

        return record


async def update_session_description(
        session_id: str,
        description: str
) -> Optional[Session]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(Session).where(Session.id == session_id)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record:
            record.description = description
            await session.flush()
            await session.refresh(record)

        return record


async def delete_by_session_id(session_id: str) -> int:
    async with connection_manager.get_connection_async() as session:
        stmt = delete(UserSessionHistory).where(
            UserSessionHistory.session_id == session_id
        )
        result = await session.execute(stmt)
        return result.rowcount


async def delete_session_with_history(session_id: str) -> bool:
    async with connection_manager.get_connection_async() as session:
        stmt = delete(Session).where(Session.id == session_id)
        result = await session.execute(stmt)
        return result.rowcount > 0


async def delete_history_record(record_id: int) -> bool:
    async with connection_manager.get_connection_async() as session:
        stmt = delete(UserSessionHistory).where(
            UserSessionHistory.id == record_id
        )
        result = await session.execute(stmt)
        return result.rowcount > 0


async def search_similar(
        embedding: List[float],
        limit: int = 10,
        session_id: Optional[str] = None
) -> Sequence[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = (
            select(UserSessionHistory)
            .where(UserSessionHistory.answer_embedding.isnot(None))
            .order_by(UserSessionHistory.answer_embedding.cosine_distance(embedding))
            .limit(limit)
        )

        if session_id:
            stmt = stmt.where(UserSessionHistory.session_id == session_id)

        result = await session.execute(stmt)
        return result.scalars().all()


async def count_session_history(session_id: str) -> int:
    async with connection_manager.get_connection_async() as session:
        stmt = select(func.count()).select_from(UserSessionHistory).where(
            UserSessionHistory.session_id == session_id
        )
        result = await session.execute(stmt)
        return result.scalar_one()


async def get_latest_history_records(
        session_id: str,
        limit: int = 10
) -> Sequence[UserSessionHistory]:
    async with connection_manager.get_connection_async() as session:
        stmt = (
            select(UserSessionHistory)
            .where(UserSessionHistory.session_id == session_id)
            .order_by(UserSessionHistory.creation_date.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
