"""AI client module - defines interface and mock implementation."""

from abc import ABC, abstractmethod


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
    """Get an AI client instance.

    Currently returns a MockClient. In the future, this will
    return a real AI client based on configuration.
    """
    return MockClient()
