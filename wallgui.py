#!/usr/bin/env python3
"""Wallpaper Manager - A modern GTK4 application for managing wallpapers."""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()
