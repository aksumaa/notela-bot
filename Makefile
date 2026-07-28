.PHONY: help install check run clean logs

help:
	@echo "Notela AI Bot - Available Commands"
	@echo "=================================="
	@echo "make install    - Install dependencies"
	@echo "make check      - Check configuration and dependencies"
	@echo "make run        - Run the bot"
	@echo "make clean      - Clean cache and logs"
	@echo "make logs       - Show bot logs"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

check:
	@echo "Checking configuration..."
	python check.py

run:
	@echo "Starting Notela AI Bot..."
	python main.py

clean:
	@echo "Cleaning project..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Project cleaned"

logs:
	@echo "Bot logs:"
	@tail -f logs/notela_bot.log 2>/dev/null || echo "No logs yet"

venv:
	@echo "Creating virtual environment..."
	python3.13 -m venv venv
	@echo "✅ Virtual environment created"
	@echo "Activate with: source venv/bin/activate"
