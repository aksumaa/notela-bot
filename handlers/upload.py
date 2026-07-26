"""
Handles incoming documents:
  - PDF file uploads -> extracted via pdf_service
  - Plain text messages -> stored as-is

Both paths end up as a Document row tied to the user.
"""
import asyncio
import logging
import os
import tempfile

from aiogram import F, Router
from aiogram.types import Message

from database.models import Document
from database.session import async_session, get_or_create_user
from locales import t
from services.ai_service import AIServiceError, transcribe_audio
from services.pdf_service import PDFExtractionError, extract_text_from_pdf

logger = logging.getLogger(__name__)
router = Router(name="upload")


@router.message(F.document)
async def handle_pdf_upload(message: Message) -> None:
    doc = message.document

    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    lang = user.language

    if not (doc.file_name or "").lower().endswith(".pdf"):
        await message.answer(t(lang, "pdf_only"))
        return

    tmp_path = None
    try:
        file_info = await message.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
        await message.bot.download_file(file_info.file_path, destination=tmp_path)

        # pdfplumber is sync/CPU-bound — keep it off the event loop.
        text = await asyncio.to_thread(extract_text_from_pdf, tmp_path)

        async with async_session() as session:
            document = Document(user_id=user.id, title=doc.file_name, raw_text=text)
            session.add(document)
            await session.commit()

        await message.answer(t(lang, "confirmation"))

    except PDFExtractionError as e:
        logger.warning("PDF extraction failed for user %s: %s", message.from_user.id, e)
        await message.answer(t(lang, "pdf_error", error=str(e)))
    except Exception:
        logger.exception("Unexpected error handling PDF upload")
        await message.answer(t(lang, "generic_error"))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.message(F.voice)
async def handle_voice_upload(message: Message) -> None:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    lang = user.language

    tmp_path = None
    await message.answer(t(lang, "transcribing_voice"))
    try:
        file_info = await message.bot.get_file(message.voice.file_id)
        with tempfile.NamedTemporaryFile(suffix=".oga", delete=False) as tmp:
            tmp_path = tmp.name
        await message.bot.download_file(file_info.file_path, destination=tmp_path)

        text = await transcribe_audio(tmp_path)

        async with async_session() as session:
            title = f"Voice note ({message.voice.duration}s)"
            document = Document(user_id=user.id, title=title, raw_text=text)
            session.add(document)
            await session.commit()

        await message.answer(t(lang, "voice_saved"))

    except AIServiceError as e:
        logger.warning("Voice transcription failed for user %s: %s", message.from_user.id, e)
        await message.answer(t(lang, "voice_error", error=str(e)))
    except Exception:
        logger.exception("Unexpected error handling voice upload")
        await message.answer(t(lang, "generic_error"))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_upload(message: Message) -> None:
    text = message.text.strip()

    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    lang = user.language

    if len(text) < 20:
        await message.answer(t(lang, "text_too_short"))
        return

    try:
        async with async_session() as session:
            title = (text[:50] + "...") if len(text) > 50 else text
            document = Document(user_id=user.id, title=title, raw_text=text)
            session.add(document)
            await session.commit()

        await message.answer(t(lang, "confirmation"))

    except Exception:
        logger.exception("Unexpected error saving text document")
        await message.answer(t(lang, "generic_error"))
