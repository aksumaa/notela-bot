"""
Integration test for Notela AI Bot.
Tests configuration, imports, and API connections.
"""

import sys
import asyncio
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_imports() -> bool:
    """Test that all imports work correctly."""
    print("Testing imports...")
    try:
        from config import Config, ConfigError, get_logger
        from main import NotelaBot
        import google.generativeai as genai
        from telegram import Update, BotCommand
        from telegram.ext import Application

        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


async def test_config() -> bool:
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from config import Config

        Config.validate()
        print(f"✅ Configuration validated")
        print(f"   - TELEGRAM_BOT_TOKEN: {'***' + Config.TELEGRAM_BOT_TOKEN[-4:]}")
        print(f"   - GEMINI_API_KEY: {'***' + Config.GEMINI_API_KEY[-4:]}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def test_logger() -> bool:
    """Test logging setup."""
    print("\nTesting logging...")
    try:
        from config import Config, get_logger

        logger = Config.setup_logging()
        test_logger = get_logger("test")

        test_logger.info("Test log message")
        print("✅ Logging setup successful")
        return True
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        return False


async def test_gemini_api() -> bool:
    """Test Gemini API configuration."""
    print("\nTesting Gemini API...")
    try:
        from config import Config
        import google.generativeai as genai

        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("✅ Gemini API configured")
        print(f"   - Model: gemini-2.0-flash")
        return True
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False


async def test_telegram_app() -> bool:
    """Test Telegram application creation."""
    print("\nTesting Telegram application...")
    try:
        from config import Config
        from telegram.ext import Application

        app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        print("✅ Telegram application created successfully")
        return True
    except Exception as e:
        print(f"❌ Telegram app test failed: {e}")
        return False


async def test_bot_instantiation() -> bool:
    """Test bot class instantiation."""
    print("\nTesting bot instantiation...")
    try:
        from main import NotelaBot

        bot = NotelaBot()
        print("✅ Bot instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Bot instantiation failed: {e}")
        return False


async def main() -> bool:
    """Run all tests."""
    print("=" * 50)
    print("Notela AI Bot - Integration Tests")
    print("=" * 50)

    tests = [
        test_imports,
        test_config,
        test_logger,
        test_gemini_api,
        test_telegram_app,
        test_bot_instantiation,
    ]

    results = []
    for test_func in tests:
        try:
            result = await test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test error: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if all(results):
        print("✅ All tests passed! Ready to deploy 🚀")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        sys.exit(1)
