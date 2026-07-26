"""
Wraps all OpenAI calls for Notela AI.

Three public functions, one per feature:
  generate_summary(text)     -> str
  generate_flashcards(text)  -> list[dict]  {"question": str, "answer": str}
  generate_quiz(text)        -> list[dict]  {"question": str, "options": [str,...], "correct_index": int}

Flashcards/quiz prompts force strict JSON output so we can parse deterministically.
"""
import json
import logging

from openai import AsyncOpenAI

from config import MAX_DOCUMENT_CHARS, OPENAI_API_KEY, OPENAI_MODEL
from locales import AI_LANGUAGE_NAME, DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def _lang_instruction(language: str) -> str:
    name = AI_LANGUAGE_NAME.get(language, AI_LANGUAGE_NAME[DEFAULT_LANGUAGE])
    return f" Respond entirely in {name}, regardless of the source material's language."


class AIServiceError(Exception):
    """Raised when an OpenAI call fails or returns unparsable content."""


def _truncate(text: str) -> str:
    if len(text) > MAX_DOCUMENT_CHARS:
        logger.warning("Document truncated from %d to %d chars", len(text), MAX_DOCUMENT_CHARS)
        return text[:MAX_DOCUMENT_CHARS]
    return text


async def _chat(system_prompt: str, user_text: str) -> str:
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.4,
        )
        content = response.choices[0].message.content
        if not content:
            raise AIServiceError("OpenAI returned an empty response.")
        return content.strip()
    except AIServiceError:
        raise
    except Exception as e:
        logger.exception("OpenAI API call failed")
        raise AIServiceError(f"OpenAI request failed: {e}") from e


def _parse_json_block(raw: str) -> dict | list:
    """Strips markdown code fences (```json ... ```) if present, then parses JSON."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse AI JSON output: %s | raw=%s", e, raw[:500])
        raise AIServiceError("AI returned malformed JSON. Please try again.") from e


async def generate_summary(text: str, language: str = DEFAULT_LANGUAGE) -> str:
    system_prompt = (
        "You are a study assistant. Summarize the given study material clearly and concisely "
        "in well-structured paragraphs or bullet points, covering the key concepts a student "
        "needs to know. Do not add information that isn't in the source text."
        + _lang_instruction(language)
    )
    return await _chat(system_prompt, _truncate(text))


async def generate_flashcards(text: str, language: str = DEFAULT_LANGUAGE) -> list[dict]:
    system_prompt = (
        "You are a study assistant. Generate 5 to 10 flashcards from the given study material. "
        "Respond with ONLY a JSON array, no other text, no markdown fences. "
        'Each item must look like: {"question": "...", "answer": "..."}'
        + _lang_instruction(language)
        + " Keep the JSON keys in English, but the question/answer VALUES must be in the target language."
    )
    raw = await _chat(system_prompt, _truncate(text))
    data = _parse_json_block(raw)

    if not isinstance(data, list) or not data:
        raise AIServiceError("AI did not return a valid flashcard list.")
    for item in data:
        if "question" not in item or "answer" not in item:
            raise AIServiceError("AI flashcard item missing required fields.")
    return data


async def transcribe_audio(file_path: str) -> str:
    """
    Transcribes a voice/audio file using OpenAI's Whisper model.
    Telegram voice messages are OGG/Opus, which Whisper accepts natively —
    no format conversion needed for this MVP.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
    except Exception as e:
        logger.exception("Whisper transcription failed for %s", file_path)
        raise AIServiceError(f"Transcription failed: {e}") from e

    text = (transcript.text or "").strip()
    if not text:
        raise AIServiceError("Transcription came back empty. Try recording again.")
    return text


async def translate_text(text: str, target_language: str) -> str:
    name = AI_LANGUAGE_NAME.get(target_language, AI_LANGUAGE_NAME[DEFAULT_LANGUAGE])
    system_prompt = (
        f"You are a translation assistant. Translate the given text into {name}. "
        "Respond with ONLY the translated text, no explanations, no quotation marks."
    )
    return await _chat(system_prompt, _truncate(text))


async def explain_topic(topic: str, language: str) -> str:
    system_prompt = (
        "You are a study assistant. Explain the given topic clearly, building intuition "
        "from first principles before adding complexity. Use simple language and a short "
        "example or analogy where useful. Keep it focused — a few paragraphs at most."
        + _lang_instruction(language)
    )
    return await _chat(system_prompt, _truncate(topic))


async def generate_quiz(text: str, language: str = DEFAULT_LANGUAGE) -> list[dict]:
    system_prompt = (
        "You are a study assistant. Generate exactly 5 multiple-choice quiz questions from the "
        "given study material. Respond with ONLY a JSON array, no other text, no markdown fences. "
        'Each item must look like: {"question": "...", "options": ["A", "B", "C", "D"], '
        '"correct_index": 0} where correct_index is the 0-based index into options.'
        + _lang_instruction(language)
        + " Keep the JSON keys in English, but the question/options VALUES must be in the target language."
    )
    raw = await _chat(system_prompt, _truncate(text))
    data = _parse_json_block(raw)

    if not isinstance(data, list) or not data:
        raise AIServiceError("AI did not return a valid quiz list.")
    for item in data:
        if "question" not in item or "options" not in item or "correct_index" not in item:
            raise AIServiceError("AI quiz item missing required fields.")
        if not isinstance(item["options"], list) or len(item["options"]) < 2:
            raise AIServiceError("AI quiz item has invalid options.")
    return data
