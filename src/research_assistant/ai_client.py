"""AI client module - defines interface and mock implementation."""

from abc import ABC, abstractmethod

from research_assistant.config import get_mode, get_model, validate_real_mode


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


def get_client() -> AIClient:
    """Get an AI client instance based on configuration.

    Returns:
        A MockClient if mode is 'mock', otherwise raises an error
        because real AI client is not implemented yet.

    Raises:
        ConfigError: If real mode is requested but API key is missing.
        NotImplementedError: If real mode is requested but not implemented.
    """
    mode = get_mode()

    if mode == "mock":
        return MockClient()

    # Real mode - validate configuration first
    validate_real_mode()

    # Real client not implemented yet
    model = get_model()
    raise NotImplementedError(
        f"Real AI client is not implemented yet. "
        f"Would use model: {model}"
    )
