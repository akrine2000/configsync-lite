"""
Core configuration sync functionality.
"""

import json
import os
from typing import Any, Dict, Optional


class ConfigSync:
    """
    Lightweight configuration manager with environment variable support.
    
    Example:
        >>> cfg = ConfigSync("config.json")
        >>> cfg.get("database.host")
        'localhost'
    """

    def __init__(self, config_path: str, env_prefix: str = "APP"):
        self.config_path = config_path
        self.env_prefix = env_prefix
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.config_path):
            return
        with open(self.config_path, "r") as f:
            self._config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value using dot notation."""
        keys = key.split(".")
        val = self._config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    def set(self, key: str, value: Any):
        """Set a config value using dot notation."""
        keys = key.split(".")
        d = self._config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def save(self):
        """Persist config to disk."""
        with open(self.config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    def all(self) -> Dict[str, Any]:
        return self._config


def load_config(path: str) -> Dict[str, Any]:
    """Load a JSON config file and return as dict."""
    with open(path, "r") as f:
        return json.load(f)


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge multiple config dicts. Later values take precedence."""
    result = {}
    for config in configs:
        _deep_merge(result, config)
    return result


def _deep_merge(base: Dict, override: Dict) -> Dict:
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base
