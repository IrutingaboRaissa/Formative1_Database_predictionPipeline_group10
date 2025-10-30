#!/usr/bin/env python3
"""MySQL Database Setup - Single Entry Point"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scripts.setup_and_populate import run_complete_setup

if __name__ == "__main__":
    sys.exit(run_complete_setup())
