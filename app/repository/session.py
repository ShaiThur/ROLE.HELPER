import uuid
from typing import List, Optional

from sqlalchemy import select, update

from common import connection_manager
from models.user_session_history import Session


async def create_session(session_id: Optional[str], user_id: str) -> Session:
    async with connection_manager.get_connection_async() as session:
        if session_id is not None:
            found_session = await get_session_by_id(session_id)
        else:
            found_session = None
        if not found_session:
            session_record = Session(
                id=str(uuid.uuid4()),
                user_id=user_id,
                description=f"сессия {str(uuid.uuid4())}",
            )
            session.add(session_record)
            await session.flush()
            await session.refresh(session_record)
            return session_record
        else:
            return found_session


async def get_sessions_by_user_id(user_id: str) -> List[Session]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(Session).where(
            Session.user_id == user_id
        )

        result = await session.execute(stmt)
        return result.scalars().all()


async def get_session_by_id(session_id: str) -> Optional[Session]:
    async with connection_manager.get_connection_async() as session:
        stmt = select(Session).where(Session.id == session_id)
        result = await session.execute(stmt)
        return result.scalars().first()


async def change_session_description(session_id: str, description: str):
    async with connection_manager.get_connection_async() as session:
        smth = update(Session).where(Session.id == session_id).values(description=description)
        await session.execute(smth)
