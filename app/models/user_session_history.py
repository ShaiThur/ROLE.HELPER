from datetime import datetime
from typing import Optional, List

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationship: one session has many history records
    user_sessions: Mapped[List["UserSessionHistory"]] = relationship(
        "UserSessionHistory",
        back_populates="session"
    )


class UserSessionHistory(Base):
    __tablename__ = "user_session_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("session.id"),
        nullable=False
    )
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    answer_embedding: Mapped[Optional[List[float]]] = mapped_column(
        Vector(1024),
        nullable=True
    )
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    is_description: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false"
    )
    intent: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped["Session"] = relationship("Session", back_populates="user_sessions")
