from contextlib import asynccontextmanager
from typing import Dict, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from common import DbConstants


class PostgresConnectionManager:
    def __init__(self, url: str, db_config: Dict[str, Any]) -> None:
        self._engine = create_async_engine(url, echo=False)
        self._factory = async_sessionmaker(self._engine, **db_config)

    @asynccontextmanager
    async def get_connection_async(self) -> AsyncSession:
        async with self._factory() as session:
            try:
                # noinspection PyTypeChecker
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            finally:
                await self._engine.dispose()


connection_manager = PostgresConnectionManager(DbConstants.DB_URL, DbConstants.DB_CONFIG)
