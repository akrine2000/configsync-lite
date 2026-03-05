"""
Environment variable interpolation for config values.
"""

import os
import re
from typing import Any, Dict


def interpolate_env(config: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Replace ${VAR} placeholders in config values with environment variables.
    
    Example:
        >>> os.environ["DB_HOST"] = "localhost"
        >>> interpolate_env({"host": "${DB_HOST}"})
        {'host': 'localhost'}
    """
    result = {}
    for k, v in config.items():
        if isinstance(v, dict):
            result[k] = interpolate_env(v, prefix)
        elif isinstance(v, str):
            result[k] = _replace_vars(v)
        else:
            result[k] = v
    return result


def _replace_vars(value: str) -> str:
    pattern = re.compile(r"\$\{([^}]+)\}")
    def replacer(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    return pattern.sub(replacer, value)
