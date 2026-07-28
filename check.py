"""
Configuration and dependency verification script.
Run this before starting the bot to check all prerequisites.
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))


def check_python_version() -> bool:
    """Check Python version compatibility."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    min_version = (3, 13)

    if version >= min_version:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (requires {min_version[0]}.{min_version[1]}+)")
        return False


def check_dependencies() -> bool:
    """Check required dependencies."""
    print("\n🔍 Checking dependencies...")
    required = {
        "telegram": "python-telegram-bot",
        "google.generativeai": "google-generativeai",
        "dotenv": "python-dotenv",
    }

    all_ok = True
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (not installed)")
            print(f"      Run: pip install -r requirements.txt")
            all_ok = False

    return all_ok


def check_environment() -> bool:
    """Check environment variables."""
    print("\n🔍 Checking environment variables...")
    from config import Config

    try:
        Config.validate()
        print(f"   ✅ TELEGRAM_BOT_TOKEN configured")
        print(f"   ✅ GEMINI_API_KEY configured")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        print(f"      Check your .env file")
        return False


def check_directories() -> bool:
    """Check required directories."""
    print("\n🔍 Checking directories...")
    required_dirs = ["handlers", "services", "utils", "database", "prompts", "storage"]

    all_ok = True
    for dirname in required_dirs:
        dirpath = Path(__file__).parent / dirname
        if dirpath.exists() and dirpath.is_dir():
            print(f"   ✅ {dirname}/")
        else:
            print(f"   ⚠️  {dirname}/ (created on startup)")

    return True


def main() -> bool:
    """Run all checks."""
    print("=" * 50)
    print("Notela AI Bot - Configuration Check")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Directories", check_directories),
    ]

    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! Game on 🚀")
        print("=" * 50)
        print("\nStart the bot with:")
        print("  python main.py")
        return True
    else:
        print("❌ Some checks failed. Fix the issues above.")
        print("=" * 50)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
