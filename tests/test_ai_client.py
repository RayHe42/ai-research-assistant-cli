"""Tests for ai_client module."""

import pytest

from research_assistant.ai_client import AIClient, ClaudeClient, MockClient, get_client
from research_assistant.config import ConfigError


def test_mock_client_is_aiclient():
    """Test that MockClient is a subclass of AIClient."""
    assert issubclass(MockClient, AIClient)


def test_claude_client_is_aiclient():
    """Test that ClaudeClient is a subclass of AIClient."""
    assert issubclass(ClaudeClient, AIClient)


def test_mock_client_summarize():
    """Test MockClient.summarize returns mock response."""
    client = MockClient()
    result = client.summarize("test prompt")
    assert "[Mock Summary]" in result


def test_mock_client_ask():
    """Test MockClient.ask returns mock response."""
    client = MockClient()
    result = client.ask("test prompt")
    assert "[Mock Answer]" in result


def test_mock_client_generate_tasks():
    """Test MockClient.generate_tasks returns mock response."""
    client = MockClient()
    result = client.generate_tasks("test prompt")
    assert "[Mock Tasks]" in result
    assert "1." in result
    assert "2." in result
    assert "3." in result


def test_get_client_returns_mock_by_default(monkeypatch):
    """Test that get_client returns MockClient when mode is mock."""
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    client = get_client()
    assert isinstance(client, MockClient)


def test_get_client_real_mode_without_key_raises(monkeypatch):
    """Test that get_client raises ConfigError in real mode without API key."""
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "real")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ConfigError, match="ANTHROPIC_API_KEY is not set"):
        get_client()


def test_get_client_real_mode_with_key(monkeypatch):
    """Test that get_client returns ClaudeClient in real mode with API key."""
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "real")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODEL", "claude-sonnet-4-20250514")
    client = get_client()
    assert isinstance(client, ClaudeClient)


def test_claude_client_init(monkeypatch):
    """Test ClaudeClient initialization."""
    # Mock anthropic.Anthropic to avoid real API call
    class MockAnthropic:
        def __init__(self, api_key):
            self.api_key = api_key

    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", MockAnthropic)
    client = ClaudeClient(api_key="test-key", model="test-model")
    assert client.model == "test-model"
    assert client.client.api_key == "test-key"


def test_claude_client_summarize(monkeypatch):
    """Test ClaudeClient.summarize calls API and returns response."""
    class MockResponse:
        content = [type("Content", (), {"text": "Test summary"})()]

    class MockMessages:
        def create(self, **kwargs):
            return MockResponse()

    class MockAnthropic:
        def __init__(self, api_key):
            self.messages = MockMessages()

    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", MockAnthropic)
    client = ClaudeClient(api_key="test-key", model="test-model")
    result = client.summarize("test prompt")
    assert result == "Test summary"


def test_claude_client_ask(monkeypatch):
    """Test ClaudeClient.ask calls API and returns response."""
    class MockResponse:
        content = [type("Content", (), {"text": "Test answer"})()]

    class MockMessages:
        def create(self, **kwargs):
            return MockResponse()

    class MockAnthropic:
        def __init__(self, api_key):
            self.messages = MockMessages()

    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", MockAnthropic)
    client = ClaudeClient(api_key="test-key", model="test-model")
    result = client.ask("test prompt")
    assert result == "Test answer"


def test_claude_client_generate_tasks(monkeypatch):
    """Test ClaudeClient.generate_tasks calls API and returns response."""
    class MockResponse:
        content = [type("Content", (), {"text": "Test tasks"})()]

    class MockMessages:
        def create(self, **kwargs):
            return MockResponse()

    class MockAnthropic:
        def __init__(self, api_key):
            self.messages = MockMessages()

    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", MockAnthropic)
    client = ClaudeClient(api_key="test-key", model="test-model")
    result = client.generate_tasks("test prompt")
    assert result == "Test tasks"
