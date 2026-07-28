"""
Notela AI - Production-Ready Telegram Bot
Conversational AI assistant powered by Google Gemini 2.0 Flash.
"""

import asyncio
import logging
import sys
from typing import Optional

import google.generativeai as genai
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import Config, ConfigError, get_logger


logger = get_logger("bot")


class NotelaBot:
    """Main Telegram bot application."""

    def __init__(self):
        """Initialize bot with configuration."""
        self.logger = logger
        self.application: Optional[Application] = None
        self.gemini_model = None

    async def initialize(self) -> None:
        """Initialize bot application and handlers."""
        self.logger.info("Initializing Notela AI Bot...")

        # Validate configuration
        Config.validate()

        # Initialize Gemini API
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel("gemini-2.0-flash")
            self.logger.info("Gemini API initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API: {e}")
            raise

        # Create Telegram application
        try:
            self.application = Application.builder().token(
                Config.TELEGRAM_BOT_TOKEN
            ).build()
            self.logger.info("Telegram application created")
        except Exception as e:
            self.logger.error(f"Failed to create Telegram application: {e}")
            raise

        # Register handlers
        self._register_handlers()

        # Set bot commands
        try:
            await self._set_bot_commands()
        except Exception as e:
            self.logger.warning(f"Failed to set bot commands: {e}")

        self.logger.info("Bot initialization completed successfully")

    def _register_handlers(self) -> None:
        """Register all command and message handlers."""
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        self.logger.debug("All handlers registered")

    async def _set_bot_commands(self) -> None:
        """Set bot commands in Telegram."""
        commands = [
            BotCommand("start", "Start the bot and get welcome message"),
            BotCommand("help", "Show help and available commands"),
        ]
        await self.application.bot.set_my_commands(commands)
        self.logger.debug("Bot commands set")

    async def handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /start command."""
        try:
            user = update.effective_user
            self.logger.info(f"User {user.id} ({user.first_name}) started bot")

            text = (
                f"🤖 Welcome to *Notela AI*, {user.first_name}\\!\n\n"
                "I'm powered by Google Gemini 2\\.0 Flash\\.\n\n"
                "📝 *Features:*\n"
                "• Chat about any topic\n"
                "• Get instant AI responses\n"
                "• Smart assistance\n\n"
                "Use /help to learn more\\."
            )

            await update.message.reply_text(text, parse_mode="MarkdownV2")

        except Exception as e:
            self.logger.error(f"Error in start command: {e}")
            try:
                await update.message.reply_text(
                    "❌ An error occurred. Please try again later."
                )
            except Exception as reply_error:
                self.logger.error(f"Failed to send error message: {reply_error}")

    async def handle_help(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /help command."""
        try:
            user = update.effective_user
            self.logger.info(f"User {user.id} requested help")

            text = (
                "📚 *Notela AI Help*\n\n"
                "*Commands:*\n"
                "/start \\- Welcome message\n"
                "/help \\- This help message\n\n"
                "*How to Use:*\n"
                "Just send me a message and I'll respond with an AI\\-powered answer\\.\n\n"
                "*Examples:*\n"
                "• What is Python\\?\n"
                "• Explain machine learning\n"
                "• How do I write a poem\\?\n"
                "• What's the weather\\?\n\n"
                "Powered by Google Gemini 2\\.0 Flash 🚀"
            )

            await update.message.reply_text(text, parse_mode="MarkdownV2")

        except Exception as e:
            self.logger.error(f"Error in help command: {e}")
            try:
                await update.message.reply_text(
                    "❌ An error occurred. Please try again later."
                )
            except Exception as reply_error:
                self.logger.error(f"Failed to send error message: {reply_error}")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle regular text messages."""
        try:
            user = update.effective_user
            message_text = update.message.text

            self.logger.info(f"Message from {user.id}: {message_text[:50]}...")

            # Show typing indicator
            await update.message.chat.send_action("typing")

            # Generate response
            response = await self._generate_response(message_text)

            if response:
                await update.message.reply_text(
                    response, parse_mode="MarkdownV2"
                )
                self.logger.debug(f"Response sent to {user.id}")
            else:
                await update.message.reply_text(
                    "Sorry, I couldn't generate a response\\. Please try again\\."
                )
                self.logger.warning(f"Empty response for user {user.id}")

        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            try:
                await update.message.reply_text(
                    "❌ An error occurred\\. Please try again later\\."
                )
            except Exception as reply_error:
                self.logger.error(f"Failed to send error message: {reply_error}")

    async def _generate_response(self, user_message: str) -> Optional[str]:
        """Generate response using Gemini API."""
        try:
            # Run blocking API call in thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_model.generate_content(user_message),
            )

            if response and response.text:
                # Escape special characters for MarkdownV2
                return self._escape_markdown(response.text)
            else:
                self.logger.warning("Empty response from Gemini API")
                return None

        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            return None

    @staticmethod
    def _escape_markdown(text: str) -> str:
        """Escape special characters for MarkdownV2."""
        special_chars = r"_*[\]()~`>#+-=|{}.!"
        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        return text

    def run(self) -> None:
        """Start the bot and run polling (blocking call)."""
        try:
            # First, initialize asynchronously
            asyncio.run(self.initialize())

            self.logger.info("=" * 50)
            self.logger.info("✅ Notela AI Bot is running!")
            self.logger.info("Press Ctrl+C to stop")
            self.logger.info("=" * 50)

            # Run polling (BLOCKING - manages its own event loop, NOT async)
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
            )

        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
            print("\n🛑 Bot stopped")

        except Exception as e:
            self.logger.critical(f"Fatal error: {e}")
            raise


def main() -> None:
    """Main entry point."""
    # Setup logging
    Config.setup_logging()

    logger.info("Starting Notela AI Bot")
    logger.debug(f"Debug mode: {Config.DEBUG}")

    bot = NotelaBot()

    try:
        # Start bot (blocking call)
        bot.run()
    except ConfigError as e:
        logger.critical(f"Configuration error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Notela AI - Telegram Bot")
    print("=" * 50)

    try:
        main()
    except KeyboardInterrupt:
        print("\n✋ Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
