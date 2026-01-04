"""Database connection management and initialization."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.infrastructure.database.models import MockDefinitionModel


class DatabaseConnection:
    """Manager for database connections and initialization."""

    def __init__(self, database_url: str):
        """Initialize database connection."""
        self.database_url = database_url
        self.engine = None
        self.async_session = None

    async def init_db(self) -> None:
        """Initialize database engine and create tables."""
        # Create async engine
        self.engine = create_async_engine(
            self.database_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
        )

        # Create async session factory
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        # Create all tables
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session generator."""
        async with self.async_session() as session:
            yield session

    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()


# Global database instance
_db_connection: DatabaseConnection = None


def init_database(database_url: str) -> DatabaseConnection:
    """Initialize and return global database connection."""
    global _db_connection
    _db_connection = DatabaseConnection(database_url)
    return _db_connection


def get_database() -> DatabaseConnection:
    """Get global database connection instance."""
    return _db_connection
