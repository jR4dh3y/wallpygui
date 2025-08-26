#!/usr/bin/env python3
from pathlib import Path

# Supported file extensions
SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".mp4", ".mkv", ".mov"}

# Cache directory and files
CACHE_DIR = Path.home() / ".cache" / "wallgui"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CACHE_DIR / "config.json"

# Default configuration (only active preferences retained)
DEFAULT_CONFIG = {
    "default_resize": "crop",
    "theme": "catppuccin"  # catppuccin, dracula, nord, gruvbox
}

# Application metadata
APP_ID = "com.example.WallpaperApp"
APP_TITLE = "Wallpaper Manager"
APP_VERSION = "2.0.0"
