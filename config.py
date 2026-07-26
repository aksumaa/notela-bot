"""
Loads configuration from environment variables (.env file).
Never hardcode secrets here — everything comes from the environment.
"""
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Optional overrides with sane defaults
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///notela.db")

# Max characters of a document we send to GPT in one call.
# Keeps prompt cost/size sane for the MVP — no chunking/RAG yet.
MAX_DOCUMENT_CHARS: int = int(os.getenv("MAX_DOCUMENT_CHARS", "12000"))


def validate_config() -> None:
    """Fail fast and loud if required secrets are missing."""
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        print(
            f"ERROR: Missing required environment variables: {', '.join(missing)}\n"
            f"Copy .env.example to .env and fill in the values."
        )
        sys.exit(1)
