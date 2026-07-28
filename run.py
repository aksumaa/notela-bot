#!/usr/bin/env python3
"""
Development run script for Notela AI Bot.
Ensures proper Python path and environment setup.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Change to project directory
os.chdir(PROJECT_ROOT)

# Import and run
if __name__ == "__main__":
    from main import main

    try:
        main()
    except KeyboardInterrupt:
        print("\n✋ Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
