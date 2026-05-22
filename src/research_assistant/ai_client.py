"""AI client module - defines interface, mock, and real implementations."""

from abc import ABC, abstractmethod

import anthropic

from research_assistant.config import get_api_key, get_mode, get_model, validate_real_mode


class AIClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    def summarize(self, prompt: str) -> str:
        """Generate a summary from the formatted prompt."""
        ...

    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Answer a question from the formatted prompt."""
        ...

    @abstractmethod
    def generate_tasks(self, prompt: str) -> str:
        """Generate follow-up study tasks from the formatted prompt."""
        ...


class MockClient(AIClient):
    """Mock AI client that returns fixed responses for testing."""

    def summarize(self, prompt: str) -> str:
        """Return a mock summary."""
        return "[Mock Summary] This is a placeholder summary. Real AI integration coming soon."

    def ask(self, prompt: str) -> str:
        """Return a mock answer."""
        return "[Mock Answer] This is a placeholder answer. Real AI integration coming soon."

    def generate_tasks(self, prompt: str) -> str:
        """Return mock study tasks."""
        return (
            "[Mock Tasks]\n"
            "1. Review the key concepts from the text\n"
            "2. Write a one-paragraph summary from memory\n"
            "3. Find 2 related articles to read"
        )


class ClaudeClient(AIClient):
    """Real AI client using Anthropic Claude API."""

    def __init__(self, api_key: str, model: str) -> None:
        """Initialize the Claude client.

        Args:
            api_key: Anthropic API key.
            model: Model name to use.
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def _call_api(self, prompt: str, max_tokens: int = 1024) -> str:
        """Call the Claude API with the given prompt.

        Args:
            prompt: The formatted prompt to send.
            max_tokens: Maximum tokens in the response.

        Returns:
            The response text from Claude.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def summarize(self, prompt: str) -> str:
        """Generate a summary using Claude API."""
        return self._call_api(prompt)

    def ask(self, prompt: str) -> str:
        """Answer a question using Claude API."""
        return self._call_api(prompt)

    def generate_tasks(self, prompt: str) -> str:
        """Generate study tasks using Claude API."""
        return self._call_api(prompt)


def get_client() -> AIClient:
    """Get an AI client instance based on configuration.

    Returns:
        A MockClient if mode is 'mock', or a ClaudeClient if mode is 'real'.

    Raises:
        ConfigError: If real mode is requested but API key is missing.
    """
    mode = get_mode()

    if mode == "mock":
        return MockClient()

    # Real mode - validate configuration first
    validate_real_mode()

    api_key = get_api_key()
    model = get_model()
    return ClaudeClient(api_key=api_key, model=model)
