"""
/help, /translate, /explain — general-purpose utility commands that don't
depend on a stored Document, unlike /summarize, /flashcards, /quiz.
"""
import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.session import async_session, get_or_create_user
from locales import t
from services.ai_service import AIServiceError, explain_topic, translate_text

logger = logging.getLogger(__name__)
router = Router(name="utility")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    await message.answer(t(user.language, "help_text"))


@router.message(Command("translate"))
async def cmd_translate(message: Message, command: CommandObject) -> None:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    lang = user.language

    if not command.args:
        await message.answer(t(lang, "translate_usage"))
        return

    await message.answer(t(lang, "translating"))
    try:
        translated = await translate_text(command.args, lang)
        await message.answer(translated)
    except AIServiceError as e:
        logger.warning("Translation failed: %s", e)
        await message.answer(t(lang, "ai_error_translate", error=str(e)))
    except Exception:
        logger.exception("Unexpected error translating text")
        await message.answer(t(lang, "generic_error"))


@router.message(Command("explain"))
async def cmd_explain(message: Message, command: CommandObject) -> None:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    lang = user.language

    if not command.args:
        await message.answer(t(lang, "explain_usage"))
        return

    await message.answer(t(lang, "explaining"))
    try:
        explanation = await explain_topic(command.args, lang)
        await message.answer(explanation)
    except AIServiceError as e:
        logger.warning("Explain failed: %s", e)
        await message.answer(t(lang, "ai_error_explain", error=str(e)))
    except Exception:
        logger.exception("Unexpected error explaining topic")
        await message.answer(t(lang, "generic_error"))
