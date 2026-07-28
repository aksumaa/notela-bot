"""
Utility functions for the Notela AI bot.
Includes string manipulation, Markdown escaping, and formatting.
"""

from typing import Optional


def escape_markdown_v2(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2 format.

    Args:
        text: Text to escape

    Returns:
        Escaped text safe for MarkdownV2
    """
    if not text:
        return ""

    # Characters that need escaping in MarkdownV2
    special_chars = r"_*[\]()~`>#+-=|{}.!"

    escaped = text
    for char in special_chars:
        escaped = escaped.replace(char, f"\\{char}")

    return escaped


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_user_name(first_name: Optional[str], last_name: Optional[str] = None) -> str:
    """
    Format user name from first and last names.

    Args:
        first_name: User's first name
        last_name: User's last name

    Returns:
        Formatted name
    """
    if not first_name:
        return "User"

    if last_name:
        return f"{first_name} {last_name}"

    return first_name


def format_log_message(user_id: int, action: str, details: str = "") -> str:
    """
    Format log message with user and action context.

    Args:
        user_id: Telegram user ID
        action: Action description
        details: Additional details

    Returns:
        Formatted log message
    """
    msg = f"User {user_id} - {action}"
    if details:
        msg += f": {details}"
    return msg
