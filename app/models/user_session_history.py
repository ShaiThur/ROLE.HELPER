from datetime import datetime
from typing import Optional, List

from sqlalchemy import BigInteger, Text, Boolean, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class UserSessionHistory(Base):
    __tablename__ = "user_session_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    answer_embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(1024), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    is_description: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    def __repr__(self) -> str:
        return (f"<UserSessionHistory(id={self.id}, session_id='{self.session_id}', "
                f"user_id='{self.user_id}')>")
