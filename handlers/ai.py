"""
/summary, /flashcards, /quiz — run the user's most recent Document through
GPT and return the result. Quiz additionally tracks an in-memory session
per user so we can score answers as inline-keyboard callbacks come in.
"""
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.models import User
from database.session import async_session, get_latest_document, get_or_create_user, save_note
from locales import t
from services.ai_service import AIServiceError, generate_flashcards, generate_quiz, generate_summary

logger = logging.getLogger(__name__)
router = Router(name="ai")

# telegram_id -> {"questions": [...], "index": int, "score": int, "language": str}
# In-memory only for this MVP: quiz progress resets if the bot restarts.
ACTIVE_QUIZZES: dict[int, dict] = {}


async def _get_user_and_document(message: Message) -> tuple[User, object]:
    async with async_session() as session:
        user = await get_or_create_user(session, message.from_user.id)
        document = await get_latest_document(session, user.id)
    if document is None:
        await message.answer(t(user.language, "no_document"))
    return user, document


@router.message(F.text == "/summarize")
async def cmd_summary(message: Message) -> None:
    user, document = await _get_user_and_document(message)
    if document is None:
        return

    await message.answer(t(user.language, "generating_summary"))
    try:
        summary = await generate_summary(document.raw_text, user.language)
        async with async_session() as session:
            await save_note(session, document.id, summary, "summary")
        await message.answer(summary)
    except AIServiceError as e:
        logger.warning("Summary generation failed: %s", e)
        await message.answer(t(user.language, "ai_error_summary", error=str(e)))
    except Exception:
        logger.exception("Unexpected error generating summary")
        await message.answer(t(user.language, "generic_error"))


@router.message(F.text == "/flashcards")
async def cmd_flashcards(message: Message) -> None:
    user, document = await _get_user_and_document(message)
    if document is None:
        return

    await message.answer(t(user.language, "generating_flashcards"))
    try:
        cards = await generate_flashcards(document.raw_text, user.language)
        formatted = "\n\n".join(
            f"Q{i+1}: {c['question']}\nA{i+1}: {c['answer']}" for i, c in enumerate(cards)
        )
        async with async_session() as session:
            await save_note(session, document.id, formatted, "flashcards")
        header = t(user.language, "flashcards_header")
        await message.answer(f"{header}\n\n{formatted}")
    except AIServiceError as e:
        logger.warning("Flashcard generation failed: %s", e)
        await message.answer(t(user.language, "ai_error_flashcards", error=str(e)))
    except Exception:
        logger.exception("Unexpected error generating flashcards")
        await message.answer(t(user.language, "generic_error"))


@router.message(F.text == "/quiz")
async def cmd_quiz(message: Message) -> None:
    user, document = await _get_user_and_document(message)
    if document is None:
        return

    await message.answer(t(user.language, "generating_quiz"))
    try:
        questions = await generate_quiz(document.raw_text, user.language)
        async with async_session() as session:
            await save_note(session, document.id, str(questions), "quiz")

        ACTIVE_QUIZZES[message.from_user.id] = {
            "questions": questions,
            "index": 0,
            "score": 0,
            "language": user.language,
        }
        await _send_quiz_question(message.chat.id, message.from_user.id, message.bot)

    except AIServiceError as e:
        logger.warning("Quiz generation failed: %s", e)
        await message.answer(t(user.language, "ai_error_quiz", error=str(e)))
    except Exception:
        logger.exception("Unexpected error generating quiz")
        await message.answer(t(user.language, "generic_error"))


async def _send_quiz_question(chat_id: int, telegram_id: int, bot) -> None:
    session_data = ACTIVE_QUIZZES[telegram_id]
    q = session_data["questions"][session_data["index"]]

    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"quiz:{i}")]
        for i, opt in enumerate(q["options"])
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    q_num = session_data["index"] + 1
    total = len(session_data["questions"])
    await bot.send_message(chat_id, f"Q{q_num}/{total}: {q['question']}", reply_markup=keyboard)


@router.callback_query(F.data.startswith("quiz:"))
async def handle_quiz_answer(callback: CallbackQuery) -> None:
    telegram_id = callback.from_user.id
    session_data = ACTIVE_QUIZZES.get(telegram_id)

    if session_data is None:
        await callback.answer(t("en", "quiz_expired"))
        return

    lang = session_data.get("language", "en")
    selected_index = int(callback.data.split(":")[1])
    q = session_data["questions"][session_data["index"]]
    correct_index = q["correct_index"]

    if selected_index == correct_index:
        session_data["score"] += 1
        await callback.answer(t(lang, "quiz_correct"))
    else:
        correct_text = q["options"][correct_index]
        await callback.answer(t(lang, "quiz_wrong", answer=correct_text), show_alert=True)

    session_data["index"] += 1
    await callback.message.edit_reply_markup(reply_markup=None)

    if session_data["index"] < len(session_data["questions"]):
        await _send_quiz_question(callback.message.chat.id, telegram_id, callback.bot)
    else:
        score = session_data["score"]
        total = len(session_data["questions"])
        await callback.message.answer(t(lang, "quiz_finished", score=score, total=total))
        del ACTIVE_QUIZZES[telegram_id]
