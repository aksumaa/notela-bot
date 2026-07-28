"""
Gemini AI service for generating responses.
Handles API calls with error handling and retry logic.
"""

import asyncio
import logging
from typing import Optional

import google.generativeai as genai

from config import get_logger


logger = get_logger("services.gemini")


class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self, api_key: str):
        """Initialize Gemini service."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        logger.info("GeminiService initialized")

    async def generate_response(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate response from Gemini API with retry logic.

        Args:
            prompt: User message to respond to
            max_retries: Maximum number of retries

        Returns:
            Generated response or None on failure
        """
        for attempt in range(max_retries):
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.model.generate_content(prompt),
                )

                if response and response.text:
                    logger.debug(f"Generated response: {response.text[:50]}...")
                    return response.text
                else:
                    logger.warning("Empty response from Gemini API")
                    return None

            except Exception as e:
                logger.warning(f"Gemini API attempt {attempt + 1}/{max_retries} failed: {e}")

                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Gemini API failed after {max_retries} attempts")
                    return None

        return None
