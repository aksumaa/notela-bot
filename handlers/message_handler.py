"""
Message handler module for processing user messages.
Demonstrates clean architecture and SOLID principles.
"""

from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

from config import get_logger


logger = get_logger("handlers.message")


class MessageHandler:
    """Handler for processing incoming messages."""

    @staticmethod
    async def handle_text_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        response_generator,
    ) -> None:
        """
        Handle incoming text messages.

        Args:
            update: Telegram update object
            context: Context object
            response_generator: Function to generate response
        """
        try:
            user = update.effective_user
            message_text = update.message.text

            logger.info(f"Processing message from user {user.id}: {message_text[:50]}...")

            # Show typing indicator
            await update.message.chat.send_action("typing")

            # Generate response
            response = await response_generator(message_text)

            if response:
                await update.message.reply_text(
                    response, parse_mode="MarkdownV2"
                )
                logger.debug(f"Response sent to user {user.id}")
            else:
                await update.message.reply_text(
                    "Sorry, I couldn't generate a response\\. Please try again\\."
                )
                logger.warning(f"Empty response for user {user.id}")

        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            try:
                await update.message.reply_text(
                    "❌ An error occurred\\. Please try again later\\."
                )
            except Exception as reply_error:
                logger.error(f"Failed to send error message: {reply_error}")
