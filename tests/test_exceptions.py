"""Tests for exceptions module."""

from research_assistant.exceptions import (
    AIClientError,
    ConfigError,
    FileLoadError,
    OutputWriteError,
    ResearchAssistantError,
)


def test_research_assistant_error_is_exception():
    """Test that ResearchAssistantError inherits from Exception."""
    assert issubclass(ResearchAssistantError, Exception)


def test_file_load_error_is_research_assistant_error():
    """Test that FileLoadError inherits from ResearchAssistantError."""
    assert issubclass(FileLoadError, ResearchAssistantError)


def test_config_error_is_research_assistant_error():
    """Test that ConfigError inherits from ResearchAssistantError."""
    assert issubclass(ConfigError, ResearchAssistantError)


def test_ai_client_error_is_research_assistant_error():
    """Test that AIClientError inherits from ResearchAssistantError."""
    assert issubclass(AIClientError, ResearchAssistantError)


def test_output_write_error_is_research_assistant_error():
    """Test that OutputWriteError inherits from ResearchAssistantError."""
    assert issubclass(OutputWriteError, ResearchAssistantError)


def test_all_errors_catchable_by_base():
    """Test that all custom errors can be caught by ResearchAssistantError."""
    for cls in [FileLoadError, ConfigError, AIClientError, OutputWriteError]:
        try:
            raise cls("test")
        except ResearchAssistantError:
            pass  # Expected


def test_error_preserves_message():
    """Test that custom errors preserve the message."""
    msg = "something went wrong"
    for cls in [ResearchAssistantError, FileLoadError, ConfigError, AIClientError, OutputWriteError]:
        err = cls(msg)
        assert str(err) == msg
