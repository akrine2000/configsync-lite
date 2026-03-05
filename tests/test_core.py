"""Tests for configsync-lite core functionality."""

import json
import os
import tempfile
import pytest

from configsync_lite import ConfigSync, load_config, merge_configs, validate_schema, interpolate_env


@pytest.fixture
def tmp_config(tmp_path):
    config = {
        "server": {"host": "localhost", "port": 8080},
        "database": {"url": "${DB_URL}", "pool_size": 5},
        "debug": False
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    return str(path)


def test_load_and_get(tmp_config):
    cfg = ConfigSync(tmp_config)
    assert cfg.get("server.host") == "localhost"
    assert cfg.get("server.port") == 8080
    assert cfg.get("debug") is False


def test_get_default(tmp_config):
    cfg = ConfigSync(tmp_config)
    assert cfg.get("nonexistent.key", default="fallback") == "fallback"


def test_set_and_save(tmp_config):
    cfg = ConfigSync(tmp_config)
    cfg.set("server.port", 9090)
    cfg.save()
    cfg2 = ConfigSync(tmp_config)
    assert cfg2.get("server.port") == 9090


def test_merge_configs():
    base = {"server": {"host": "localhost", "port": 8080}, "debug": False}
    override = {"server": {"port": 9090}, "debug": True}
    merged = merge_configs(base, override)
    assert merged["server"]["host"] == "localhost"
    assert merged["server"]["port"] == 9090
    assert merged["debug"] is True


def test_interpolate_env(tmp_config):
    os.environ["DB_URL"] = "postgresql://localhost/mydb"
    raw = load_config(tmp_config)
    resolved = interpolate_env(raw)
    assert resolved["database"]["url"] == "postgresql://localhost/mydb"


def test_validate_schema_valid(tmp_config):
    config = {"host": "localhost", "port": 8080, "debug": True}
    schema = {
        "host": {"type": "str", "required": True},
        "port": {"type": "int", "required": True},
        "debug": {"type": "bool", "required": False}
    }
    errors = validate_schema(config, schema)
    assert errors == []


def test_validate_schema_missing_required():
    config = {"port": 8080}
    schema = {"host": {"type": "str", "required": True}}
    errors = validate_schema(config, schema)
    assert len(errors) == 1
    assert "host" in errors[0]


def test_validate_schema_wrong_type():
    config = {"port": "not-an-int"}
    schema = {"port": {"type": "int", "required": True}}
    errors = validate_schema(config, schema)
    assert len(errors) == 1
