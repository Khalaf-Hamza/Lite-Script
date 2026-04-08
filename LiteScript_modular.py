#!/usr/bin/env python3
"""
LiteScript Modular Runner
"""
import sys
import os

# Get the absolute path of the 'litescript_core' directory
core_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'litescript_core')

# Add 'litescript_core' to sys.path so we can import modules from it directly
sys.path.insert(0, core_dir)

from Main import main

if __name__ == "__main__":
    main()
