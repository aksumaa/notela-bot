# Notela AI

An AI study assistant Telegram bot. Send it a PDF or plain text, then generate
a summary, flashcards, or a multiple-choice quiz from it.

## Features

- `/start` — greets you, creates your user record, shows a quick-access keyboard
- `/help` — lists all commands
- `/settings` — switch UI and AI response language between 🇺🇿 Uzbek, 🇷🇺 Russian, 🇬🇧 English
- Send a **PDF** — bot extracts the text and stores it as a Document
- Send a **voice message** — transcribed via Whisper and stored as a Document
- Send **plain text** — stored as a Document too
- `/summarize` — GPT summary of your most recent Document
- `/flashcards` — 5–10 Q&A flashcards from your most recent Document
- `/quiz` — 5 multiple-choice questions, one at a time, with score tracking
- `/translate <text>` — translate any text into your current language
- `/explain <topic>` — explain any topic simply, from first principles

All AI features respect your chosen `/settings` language — summaries, flashcards,
quiz questions, translations, and explanations are generated in Uzbek, Russian,
or English accordingly. The bot's `/` command menu and the persistent bottom
keyboard (shown after `/start`) give quick access to every command.

> **Upgrading from an earlier version?** Delete your existing `notela.db` before
> running the bot again — a new `language` column was added to the `users` table
> and this MVP doesn't include a migration tool (see Limitations below).

## Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An OpenAI API key

## Setup

1. **Clone / copy the project, then create a virtual environment:**

   ```bash
   cd notela
   python3.11 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Then open `.env` and fill in:
   - `BOT_TOKEN` — from BotFather
   - `OPENAI_API_KEY` — from OpenAI

4. **Run the bot:**

   ```bash
   python bot.py
   ```

   On first run this creates `notela.db` (SQLite) in the project directory
   with the required tables.

5. **Use it:** open your bot in Telegram, send `/start`, then send it a PDF
   or some text, followed by `/summary`, `/flashcards`, or `/quiz`.

## Project structure

```
notela/
  bot.py              # entrypoint, starts polling
  config.py           # loads .env
  database/
    models.py         # User, Document, Note ORM models
    session.py        # async engine/session + query helpers
  handlers/
    start.py          # /start
    upload.py         # PDF + text ingestion
    ai.py             # /summary, /flashcards, /quiz
  services/
    pdf_service.py     # pdfplumber text extraction
    ai_service.py       # OpenAI calls + JSON parsing
  requirements.txt
  .env.example
```

## Notes & limitations (by design, for this MVP)

- Only **one active Document per action** is used — always the most
  recently uploaded one. There's no document picker yet.
- **Scanned/image-only PDFs are not supported** (no OCR yet) — you'll get
  an error if no text can be extracted.
- Quiz progress is kept **in memory**, not in the database — restarting the
  bot mid-quiz will end that quiz session (final results aren't scored).
- Documents longer than `MAX_DOCUMENT_CHARS` (default 12,000) are truncated
  before being sent to GPT — no chunking/RAG in this version.
- No OCR, board/photo scanning, YouTube ingestion, presentations, scheduling,
  spaced repetition, or analytics yet — these are on the roadmap, one at a time.
- Voice notes are sent to Whisper as-is (OGG/Opus) — no format conversion or
  chunking, so very long recordings may hit API limits.
- No database migrations (e.g. Alembic) — schema changes like the new
  `language` column mean deleting `notela.db` during development. Add
  migrations before this goes to real users.

## Troubleshooting

- **Bot doesn't respond:** check `BOT_TOKEN` is correct and the bot isn't
  running elsewhere (Telegram only allows one polling instance at a time).
- **OpenAI errors:** check `OPENAI_API_KEY` is valid and has quota.
- **"No extractable text found" on a PDF:** it's likely a scanned image PDF;
  try a text-based PDF instead.
