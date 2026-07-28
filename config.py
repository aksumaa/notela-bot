"""
Configuration module for Notela AI Telegram Bot.
Loads and validates environment variables with proper error handling.
"""

import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv


# Load .env file
ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(ENV_FILE)


class ConfigError(Exception):
    """Configuration validation error."""
    pass


class Config:
    """Application configuration with validation."""

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()

    # Application
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Directories
    LOG_DIR: Path = Path(__file__).parent / "logs"
    DATABASE_DIR: Path = Path(__file__).parent / "storage"

    @classmethod
    def validate(cls) -> None:
        """Validate all required configuration."""
        errors = []

        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required in .env")

        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required in .env")

        if cls.LOG_LEVEL not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            errors.append(f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}")

        if errors:
            error_msg = "\n".join(errors)
            raise ConfigError(f"Configuration validation failed:\n{error_msg}")

    @classmethod
    def setup_logging(cls) -> logging.Logger:
        """Configure logging with file and console handlers."""
        cls.LOG_DIR.mkdir(exist_ok=True, parents=True)

        logger = logging.getLogger("notela")
        logger.setLevel(cls.LOG_LEVEL)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        log_file = cls.LOG_DIR / "notela_bot.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(f"notela.{name}")
