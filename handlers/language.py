"""
/language — lets the user switch the bot's UI and AI-response language
between Uzbek, Russian, and English via inline buttons.
"""
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.session import async_session, get_or_create_user, set_user_language
from locales import LANGUAGE_LABELS, SUPPORTED_LANGUAGES, t

logger = logging.getLogger(__name__)
router = Router(name="language")


def _language_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=LANGUAGE_LABELS[code], callback_data=f"lang:{code}")]
        for code in SUPPORTED_LANGUAGES
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == "/settings")
async def cmd_language(message: Message) -> None:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
    await message.answer(t(user.language, "language_prompt"), reply_markup=_language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def handle_language_choice(callback: CallbackQuery) -> None:
    language = callback.data.split(":")[1]

    if language not in SUPPORTED_LANGUAGES:
        await callback.answer("Unsupported language.")
        return

    try:
        async with async_session() as session:
            await set_user_language(session, callback.from_user.id, language)
    except Exception:
        logger.exception("Failed to update language for user %s", callback.from_user.id)
        await callback.answer("Something went wrong. Try again.")
        return

    await callback.answer()
    await callback.message.edit_text(t(language, "language_set"))
