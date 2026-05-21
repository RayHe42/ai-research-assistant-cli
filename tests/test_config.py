"""Tests for config module."""

import pytest

from research_assistant.config import (
    DEFAULT_MODE,
    DEFAULT_MODEL,
    ENV_API_KEY,
    ENV_MODE,
    ENV_MODEL,
    ConfigError,
    get_api_key,
    get_mode,
    get_model,
    validate_real_mode,
)


def test_default_mode_is_mock(monkeypatch):
    """Test that default mode is 'mock' when env var is not set."""
    monkeypatch.delenv(ENV_MODE, raising=False)
    assert get_mode() == DEFAULT_MODE


def test_read_mode_from_env(monkeypatch):
    """Test reading mode from environment variable."""
    monkeypatch.setenv(ENV_MODE, "real")
    assert get_mode() == "real"


def test_mode_is_case_insensitive(monkeypatch):
    """Test that mode comparison is case-insensitive."""
    monkeypatch.setenv(ENV_MODE, "REAL")
    assert get_mode() == "real"


def test_invalid_mode_raises_error(monkeypatch):
    """Test that invalid mode raises ConfigError."""
    monkeypatch.setenv(ENV_MODE, "invalid")
    with pytest.raises(ConfigError, match="Invalid"):
        get_mode()


def test_default_api_key_is_none(monkeypatch):
    """Test that default API key is None."""
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    assert get_api_key() is None


def test_read_api_key_from_env(monkeypatch):
    """Test reading API key from environment variable."""
    monkeypatch.setenv(ENV_API_KEY, "test-key-123")
    assert get_api_key() == "test-key-123"


def test_default_model(monkeypatch):
    """Test that default model is 'mock-model'."""
    monkeypatch.delenv(ENV_MODEL, raising=False)
    assert get_model() == DEFAULT_MODEL


def test_read_model_from_env(monkeypatch):
    """Test reading model from environment variable."""
    monkeypatch.setenv(ENV_MODEL, "gpt-4")
    assert get_model() == "gpt-4"


def test_real_mode_without_key_raises_error(monkeypatch):
    """Test that real mode without API key raises ConfigError."""
    monkeypatch.setenv(ENV_MODE, "real")
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    with pytest.raises(ConfigError, match="RESEARCH_ASSISTANT_API_KEY is not set"):
        validate_real_mode()


def test_real_mode_with_key_passes(monkeypatch):
    """Test that real mode with API key passes validation."""
    monkeypatch.setenv(ENV_MODE, "real")
    monkeypatch.setenv(ENV_API_KEY, "test-key-123")
    validate_real_mode()  # Should not raise


def test_mock_mode_ignores_missing_key(monkeypatch):
    """Test that mock mode works without API key."""
    monkeypatch.setenv(ENV_MODE, "mock")
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    validate_real_mode()  # Should not raise
