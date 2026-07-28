..[p# Notela AI - Development Guide

## Project Overview

Notela AI is a production-ready Telegram bot powered by Google Gemini 2.0 Flash. The codebase follows Clean Architecture principles and SOLID design patterns.

## Architecture

### Layers

1. **Presentation Layer** (`main.py`)
   - Telegram bot interface
   - Command handlers
   - User message processing
   - Message formatting and escaping

2. **Service Layer** (`services/`)
   - Business logic
   - API interactions
   - Data processing
   - Example: `GeminiService` for AI responses

3. **Data Layer** (`database.py`)
   - SQLite database management
   - User data storage
   - Message history
   - Schema management

4. **Utilities** (`utils/`)
   - String manipulation
   - Formatting helpers
   - Common functions

5. **Configuration** (`config.py`)
   - Environment variable management
   - Logging setup
   - Validation

## Key Design Patterns

### 1. Async/Await Pattern
All I/O operations use async/await to handle concurrent requests efficiently.

```python
async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await self.message.reply_text("response")
```

### 2. Service Layer Pattern
Business logic is separated into service classes.

```python
from services.gemini_service import GeminiService

gemini = GeminiService(api_key)
response = await gemini.generate_response(prompt)
```

### 3. Dependency Injection
Configuration and services are injected to avoid tight coupling.

```python
from config import Config

api_key = Config.GEMINI_API_KEY
```

### 4. Error Handling
Comprehensive error handling with logging at each layer.

```python
try:
    response = await generate_response(message)
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
```

## Adding New Handlers

### Step 1: Create Handler Module

`handlers/new_command.py`:
```python
from telegram import Update
from telegram.ext import ContextTypes
from config import get_logger

logger = get_logger("handlers.new_command")

class NewCommandHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Your logic here
            await update.message.reply_text("Response")
        except Exception as e:
            logger.error(f"Error: {e}")
```

### Step 2: Register in main.py

In `NotelaBot._register_handlers()`:
```python
from handlers.new_command import NewCommandHandler

self.application.add_handler(
    CommandHandler("newcommand", NewCommandHandler.handle)
)
```

## Adding New Services

### Step 1: Create Service Module

`services/my_service.py`:
```python
from config import get_logger

logger = get_logger("services.my_service")

class MyService:
    def __init__(self):
        logger.info("MyService initialized")
    
    async def do_something(self, data):
        try:
            # Process data
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
            raise
```

### Step 2: Use in Handlers

```python
from services.my_service import MyService

service = MyService()
result = await service.do_something(data)
```

## Configuration Management

### Adding New Config Variables

1. Add to `.env`:
```
NEW_SETTING=value
```

2. Add to `config.py`:
```python
class Config:
    NEW_SETTING: str = os.getenv("NEW_SETTING", "default_value")
```

3. Validation:
```python
@classmethod
def validate(cls):
    if not cls.NEW_SETTING:
        raise ConfigError("NEW_SETTING is required")
```

## Logging

### Logger Usage

```python
from config import get_logger

logger = get_logger("module_name")

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Log Files

- File: `logs/notela_bot.log`
- Console: stdout

## Database

### Using Database

```python
from database import Database

with Database() as db:
    db.connect()
    db.initialize_schema()
    
    # Use db.connection for queries
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users")
```

## Testing

### Run Integration Tests

```bash
python test_integration.py
```

### Run Configuration Check

```bash
python check.py
```

## Best Practices

### 1. Always Use Async for I/O
```python
# Good
response = await asyncio.to_thread(blocking_function)

# Bad
response = blocking_function()  # Blocks event loop
```

### 2. Escape Markdown in Responses
```python
from utils.string_utils import escape_markdown_v2

safe_text = escape_markdown_v2(user_text)
await message.reply_text(safe_text, parse_mode="MarkdownV2")
```

### 3. Use Logging Everywhere
```python
logger.info(f"User {user_id} executed action")
logger.error(f"Error occurred: {e}", exc_info=True)
```

### 4. Handle Exceptions Gracefully
```python
try:
    # operations
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    # Handle gracefully
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    # Return user-friendly message
```

### 5. Use Type Hints
```python
async def generate_response(message: str) -> Optional[str]:
    try:
        # Generate response
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
```

## Common Issues

### Issue: Event Loop Already Running

**Solution**: Use `run_executor` for blocking operations:
```python
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(None, blocking_function)
```

### Issue: API Key Not Found

**Solution**: Check `.env` file:
```bash
python check.py
```

### Issue: Gemini API Timeout

**Solution**: Increase timeout or add retry logic:
```python
for attempt in range(max_retries):
    try:
        response = await generate()
        break
    except Exception as e:
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)
```

## Performance

### Optimization Tips

1. **Use Thread Pool for Blocking Operations**
   - API calls
   - Database queries
   - File I/O

2. **Cache Results**
   - User settings
   - API responses
   - Configuration

3. **Batch Operations**
   - Database inserts
   - Message updates

4. **Monitor Logs**
   - Watch for errors
   - Track performance metrics
   - Identify bottlenecks

## Deployment

### Pre-deployment Checklist

- [ ] Run `python check.py`
- [ ] Run `python test_integration.py`
- [ ] Check `.env` file has all required variables
- [ ] Review logs for errors
- [ ] Verify API keys are valid

### Production Deployment

1. Set `LOG_LEVEL=WARNING`
2. Set `DEBUG=False`
3. Secure `.env` file permissions
4. Monitor logs and errors
5. Set up error alerting

## Resources

- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Google Generative AI](https://ai.google.dev/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

## Support

For issues:
1. Check logs: `tail -f logs/notela_bot.log`
2. Run checks: `python check.py`
3. Run tests: `python test_integration.py`
4. Review error traceback in logs

---

Happy coding! 🚀
