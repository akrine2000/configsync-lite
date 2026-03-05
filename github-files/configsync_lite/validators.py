"""
Schema validation for configuration files.
"""

from typing import Any, Dict, List, Optional


def validate_schema(config: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Validate a config dict against a simple schema.
    Returns a list of validation errors (empty if valid).
    
    Schema format:
        {
            "field_name": {"type": "str", "required": True},
            "port": {"type": "int", "required": False, "default": 8080}
        }
    """
    errors = []
    for field, rules in schema.items():
        value = config.get(field)
        required = rules.get("required", False)
        expected_type = rules.get("type")

        if value is None:
            if required:
                errors.append(f"Missing required field: '{field}'")
            continue

        type_map = {"str": str, "int": int, "float": float, "bool": bool, "list": list, "dict": dict}
        if expected_type and expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                errors.append(f"Field '{field}' expected {expected_type}, got {type(value).__name__}")

    return errors
