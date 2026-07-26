"""
Notela AI — entrypoint.
Run with: python bot.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN, validate_config
from database.session import init_db
from handlers import ai, language, start, upload, utility
from locales import BOT_COMMANDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def _setup_commands(bot: Bot) -> None:
    """
    Populates Telegram's "/" command menu. Registered per language_code so
    the menu matches each user's Telegram client language, plus a global
    English fallback for anything else.
    """
    for lang_code, commands in BOT_COMMANDS.items():
        bot_commands = [BotCommand(command=c, description=d) for c, d in commands]
        await bot.set_my_commands(
            bot_commands, scope=BotCommandScopeDefault(), language_code=lang_code
        )
    await bot.set_my_commands(
        [BotCommand(command=c, description=d) for c, d in BOT_COMMANDS["en"]],
        scope=BotCommandScopeDefault(),
    )


async def main() -> None:
    validate_config()
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Order matters: command handlers before the generic text catch-all.
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(utility.router)
    dp.include_router(ai.router)
    dp.include_router(upload.router)

    await _setup_commands(bot)

    logger.info("Starting Notela AI bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
