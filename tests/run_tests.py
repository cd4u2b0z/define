#!/usr/bin/env python3
"""
Run all tests for the define dictionary tool.

Usage:
    python -m pytest tests/ -v          # With pytest (recommended)
    python tests/run_tests.py           # With unittest
    python tests/run_tests.py -v        # Verbose mode
"""

import sys
import unittest
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_tests(verbosity=1):
    """Discover and run all tests."""
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=Path(__file__).parent,
        pattern="test_*.py"
    )
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    verbosity = 2 if "-v" in sys.argv or "--verbose" in sys.argv else 1
    sys.exit(run_tests(verbosity))
