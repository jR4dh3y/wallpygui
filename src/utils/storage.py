#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any, Dict


class StorageManager:
    """Handles all file storage operations for the application."""
    
    @staticmethod
    def load_json(path: Path, default: Any = None) -> Any:
        """Load data from a JSON file."""
        try:
            if path.exists():
                return json.loads(path.read_text())
        except Exception as e:
            print(f"Failed to load {path}: {e}")
        return default
    
    @staticmethod
    def save_json(path: Path, data: Any) -> bool:
        """Save data to a JSON file."""
        try:
            path.write_text(json.dumps(data, indent=2))
            return True
        except Exception as e:
            print(f"Failed to save {path}: {e}")
            return False
    
    @staticmethod
    
    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load application configuration."""
        from utils.constants import CONFIG_FILE, DEFAULT_CONFIG
        config = StorageManager.load_json(CONFIG_FILE, default=DEFAULT_CONFIG)
        # Ensure all default keys exist
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        return config
    
    @staticmethod
    def save_config(config: Dict[str, Any]) -> bool:
        """Save application configuration."""
        from utils.constants import CONFIG_FILE
        return StorageManager.save_json(CONFIG_FILE, config)
