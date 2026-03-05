"""
configsync-lite: A lightweight configuration sync utility for Python projects.
Supports JSON, YAML, and TOML configuration files with environment variable interpolation.
"""

__version__ = "0.1.2"
__author__ = "optimusdemo"

from .core import ConfigSync, load_config, merge_configs
from .validators import validate_schema
from .env import interpolate_env

__all__ = ["ConfigSync", "load_config", "merge_configs", "validate_schema", "interpolate_env"]
