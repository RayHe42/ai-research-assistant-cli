"""Configuration module - reads settings from environment variables."""

import os

# Environment variable names
ENV_MODE = "RESEARCH_ASSISTANT_MODE"
ENV_API_KEY = "RESEARCH_ASSISTANT_API_KEY"
ENV_MODEL = "RESEARCH_ASSISTANT_MODEL"

# Default values
DEFAULT_MODE = "mock"
DEFAULT_MODEL = "mock-model"

# Valid modes
VALID_MODES = {"mock", "real"}


class ConfigError(Exception):
    """Raised when configuration is invalid."""


def get_mode() -> str:
    """Get the AI mode from environment variable.

    Returns:
        The mode string: 'mock' or 'real'.
    """
    mode = os.environ.get(ENV_MODE, DEFAULT_MODE).lower()
    if mode not in VALID_MODES:
        raise ConfigError(
            f"Invalid {ENV_MODE}={mode!r}. "
            f"Must be one of: {', '.join(sorted(VALID_MODES))}"
        )
    return mode


def get_api_key() -> str | None:
    """Get the API key from environment variable.

    Returns:
        The API key string, or None if not set.
    """
    return os.environ.get(ENV_API_KEY)


def get_model() -> str:
    """Get the model name from environment variable.

    Returns:
        The model name string.
    """
    return os.environ.get(ENV_MODEL, DEFAULT_MODEL)


def validate_real_mode() -> None:
    """Validate that real mode has required configuration.

    Raises:
        ConfigError: If real mode is requested but API key is missing.
    """
    mode = get_mode()
    api_key = get_api_key()

    if mode == "real" and not api_key:
        raise ConfigError(
            f"{ENV_MODE} is 'real', but {ENV_API_KEY} is not set.\n"
            f"Please set your API key:\n"
            f"  export {ENV_API_KEY}=\"your-key-here\"\n"
            f"Or use mock mode:\n"
            f"  export {ENV_MODE}=\"mock\""
        )
