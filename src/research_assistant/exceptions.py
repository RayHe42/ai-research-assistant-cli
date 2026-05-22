"""Custom exceptions for AI Research Assistant."""


class ResearchAssistantError(Exception):
    """Base exception for all AI Research Assistant errors."""


class FileLoadError(ResearchAssistantError):
    """Raised when a file cannot be loaded (not found, unsupported format, empty)."""


class ConfigError(ResearchAssistantError):
    """Raised when configuration is invalid or missing."""


class AIClientError(ResearchAssistantError):
    """Raised when AI client call fails."""


class OutputWriteError(ResearchAssistantError):
    """Raised when output cannot be saved to file."""
