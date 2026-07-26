"""
Async engine / session factory + a couple of small data-access helpers
used by the handlers. Keeping these here avoids duplicating queries.
"""
import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DATABASE_URL
from database.models import Base, Document, Note, User

logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Create tables if they don't exist yet. Call once on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized at %s", DATABASE_URL)


async def get_or_create_user(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info("Created new user telegram_id=%s", telegram_id)
    return user


async def set_user_language(session: AsyncSession, telegram_id: int, language: str) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=telegram_id, language=language)
        session.add(user)
    else:
        user.language = language
    await session.commit()
    await session.refresh(user)
    return user


async def get_latest_document(session: AsyncSession, user_id: int) -> Optional[Document]:
    result = await session.execute(
        select(Document)
        .where(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def save_note(session: AsyncSession, document_id: int, content: str, note_type: str) -> Note:
    note = Note(document_id=document_id, content=content, type=note_type)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note
