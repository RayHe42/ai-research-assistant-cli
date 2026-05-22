"""Tests for ai_client module."""

import anthropic
import pytest

from research_assistant.ai_client import AIClient, ClaudeClient, MockClient, get_client
from research_assistant.exceptions import AIClientError, ConfigError


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


def _make_mock_anthropic(exception_cls, message):
    """Create a mock Anthropic client that raises the given exception."""

    class MockMessages:
        def create(self, **kwargs):
            raise exception_cls(message)

    class MockAnthropic:
        def __init__(self, api_key):
            self.messages = MockMessages()

    return MockAnthropic


def test_claude_client_auth_error_raises_ai_client_error(monkeypatch):
    """Test that AuthenticationError is wrapped in AIClientError."""
    # Use a simple subclass to avoid httpx.Response requirement
    class FakeAuthError(anthropic.AuthenticationError):
        def __init__(self, message):
            Exception.__init__(self, message)

    mock_cls = _make_mock_anthropic(FakeAuthError, "invalid key")
    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", mock_cls)
    client = ClaudeClient(api_key="test-key", model="test-model")
    with pytest.raises(AIClientError, match="authentication failed"):
        client.summarize("test prompt")


def test_claude_client_rate_limit_raises_ai_client_error(monkeypatch):
    """Test that RateLimitError is wrapped in AIClientError."""
    class FakeRateLimitError(anthropic.RateLimitError):
        def __init__(self, message):
            Exception.__init__(self, message)

    mock_cls = _make_mock_anthropic(FakeRateLimitError, "rate limited")
    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", mock_cls)
    client = ClaudeClient(api_key="test-key", model="test-model")
    with pytest.raises(AIClientError, match="rate limit"):
        client.ask("test prompt")


def test_claude_client_api_error_raises_ai_client_error(monkeypatch):
    """Test that APIError is wrapped in AIClientError."""
    class FakeAPIError(anthropic.APIError):
        def __init__(self, message):
            Exception.__init__(self, message)

    mock_cls = _make_mock_anthropic(FakeAPIError, "server error")
    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", mock_cls)
    client = ClaudeClient(api_key="test-key", model="test-model")
    with pytest.raises(AIClientError, match="API call failed"):
        client.generate_tasks("test prompt")


def test_claude_client_api_error_does_not_leak_details(monkeypatch):
    """Test that APIError message does not leak internal details."""
    class FakeAPIError(anthropic.APIError):
        def __init__(self, message):
            Exception.__init__(self, message)

    mock_cls = _make_mock_anthropic(FakeAPIError, "internal server detail: req-abc-123")
    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", mock_cls)
    client = ClaudeClient(api_key="test-key", model="test-model")
    with pytest.raises(AIClientError) as exc_info:
        client.summarize("test prompt")
    assert "req-abc-123" not in str(exc_info.value)


def test_claude_client_error_does_not_leak_api_key(monkeypatch):
    """Test that AIClientError message does not contain the API key."""
    class FakeAuthError(anthropic.AuthenticationError):
        def __init__(self, message):
            Exception.__init__(self, message)

    mock_cls = _make_mock_anthropic(FakeAuthError, "invalid key")
    monkeypatch.setattr("research_assistant.ai_client.anthropic.Anthropic", mock_cls)
    secret_key = "sk-ant-secret-key-12345"
    client = ClaudeClient(api_key=secret_key, model="test-model")
    with pytest.raises(AIClientError) as exc_info:
        client.summarize("test prompt")
    assert secret_key not in str(exc_info.value)
