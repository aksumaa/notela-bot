"""
/start command — greets the user and ensures a User row exists.
"""
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from database.session import async_session, get_or_create_user
from locales import t

logger = logging.getLogger(__name__)
router = Router(name="start")


def _main_keyboard() -> ReplyKeyboardMarkup:
    """
    Persistent bottom keyboard for quick access to the core commands.
    Buttons send the plain command text (e.g. "/summarize") so they're
    routed by the exact same handlers as if the user had typed it.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/summarize"), KeyboardButton(text="/quiz")],
            [KeyboardButton(text="/flashcards"), KeyboardButton(text="/translate")],
            [KeyboardButton(text="/explain"), KeyboardButton(text="/settings")],
        ],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    try:
        async with async_session() as session:
            user = await get_or_create_user(session, message.from_user.id)
    except Exception:
        logger.exception("Failed to create/fetch user on /start")
        await message.answer("Something went wrong on my end. Please try again in a moment.")
        return

    await message.answer(t(user.language, "welcome"), reply_markup=_main_keyboard())
