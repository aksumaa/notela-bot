# Notela AI - Telegram Bot

A production-ready Telegram bot powered by Google Gemini 2.0 Flash AI.

## Features

- ✅ Fully asynchronous architecture
- ✅ Google Gemini 2.0 Flash integration
- ✅ Clean Architecture & SOLID principles
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Production-ready deployment
- ✅ Command support: `/start`, `/help`
- ✅ Message handling with AI responses

## Requirements

- Python 3.13+
- python-telegram-bot 22.x
- Google Gemini API key
- Telegram Bot Token

## Installation

1. **Clone the repository**
   ```bash
   cd notela-bot
   ```

2. **Create virtual environment**
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Create `.env` file with:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   GEMINI_API_KEY=your_gemini_key_here
   LOG_LEVEL=INFO
   DEBUG=False
   ```

## Usage

Start the bot:
```bash
python main.py
```

The bot will:
- Connect to Telegram
- Initialize Gemini API
- Start polling for messages
- Respond to `/start`, `/help`, and user messages

## Project Structure

```
notela-bot/
├── main.py              # Main bot application
├── config.py            # Configuration management
├── database.py          # Database initialization
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── logs/               # Application logs
├── storage/            # SQLite database
├── handlers/           # Message handlers
├── services/           # Business logic
├── utils/              # Utilities
├── database/           # Database models
└── prompts/            # AI prompts
```

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)
- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `DEBUG` - Enable debug mode (True/False)

## Logging

Logs are stored in `logs/notela_bot.log` and displayed in console.

## Architecture

### Design Patterns
- **Async/Await**: Full asyncio support
- **Singleton**: Configuration management
- **Factory**: Logger creation
- **Strategy**: Message handling

### Clean Architecture
- Separated concerns
- Dependency injection ready
- Testable code structure
- Clear layer separation

## Performance

- Handles multiple concurrent users
- Non-blocking I/O with asyncio
- Efficient API calls with thread pooling
- Graceful error recovery

## Security

- API keys not exposed in logs
- Input validation
- Markdown escaping for message safety
- No hardcoded credentials

## Development

### Adding New Handlers

1. Create handler in `handlers/`
2. Register in `main.py` NotelaBot class
3. Test with bot commands

### Adding Services

1. Create service in `services/`
2. Implement business logic
3. Use in handlers

## Troubleshooting

### Bot not connecting
- Check `TELEGRAM_BOT_TOKEN` is correct
- Verify internet connection
- Check logs in `logs/notela_bot.log`

### Gemini API errors
- Verify `GEMINI_API_KEY` is valid
- Check API quota
- Review error logs

### Port conflicts
- Change polling method if needed
- Check firewall settings

## License

MIT

## Support

For issues and questions, check logs or review the code documentation.

---

**Powered by Google Gemini 2.0 Flash**
