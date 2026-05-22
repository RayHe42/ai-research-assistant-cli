"""Tests for CLI error handling."""

import logging

import pytest

from research_assistant.cli import main
from research_assistant.exceptions import (
    AIClientError,
    ConfigError,
    FileLoadError,
    OutputWriteError,
)
from research_assistant.logger import LOGGER_NAME


@pytest.fixture(autouse=True)
def reset_logger():
    """Reset logger state between tests to avoid handler leaks."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    yield
    logger.handlers.clear()


def test_main_importable():
    """Test that main is importable and callable."""
    assert callable(main)


def test_file_not_found_shows_friendly_error(monkeypatch, capsys):
    """Test that missing file shows friendly error, not traceback."""
    monkeypatch.setattr("sys.argv", ["research", "summarize", "/nonexistent/file.txt"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "File not found" in captured.err
    assert "Traceback" not in captured.err


def test_unsupported_file_type_shows_friendly_error(monkeypatch, tmp_path, capsys):
    """Test that unsupported file type shows friendly error."""
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("a,b,c")
    monkeypatch.setattr("sys.argv", ["research", "summarize", str(csv_file)])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "Unsupported file type" in captured.err


def test_empty_file_shows_friendly_error(monkeypatch, tmp_path, capsys):
    """Test that empty file shows friendly error."""
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("")
    monkeypatch.setattr("sys.argv", ["research", "summarize", str(empty_file)])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "empty" in captured.err.lower()


def test_config_error_shows_friendly_error(monkeypatch, capsys):
    """Test that config error shows friendly error."""
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "real")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr("sys.argv", ["research", "summarize", "examples/sample_note.md"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "ANTHROPIC_API_KEY" in captured.err


def test_verbose_flag_accepted(monkeypatch, tmp_path):
    """Test that --verbose flag is accepted by the CLI."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "--verbose", "summarize", str(note)])
    main()  # Should not raise


def test_verbose_short_flag_accepted(monkeypatch, tmp_path):
    """Test that -v short flag is accepted."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "-v", "summarize", str(note)])
    main()  # Should not raise


def test_verbose_unknown_exception_shows_traceback(monkeypatch, tmp_path, capsys):
    """Test that --verbose shows traceback for unknown exceptions."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "--verbose", "summarize", str(note)])

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("research_assistant.cli.build_summarize_prompt", boom)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.err


def test_non_verbose_unknown_exception_shows_generic_message(monkeypatch, tmp_path, capsys):
    """Test that non-verbose mode shows generic error for unknown exceptions."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "summarize", str(note)])

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("research_assistant.cli.build_summarize_prompt", boom)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "unexpected error" in captured.err.lower()
    assert "--verbose" in captured.err


def test_output_write_error_shows_friendly_error(monkeypatch, tmp_path, capsys):
    """Test that output write error shows friendly error."""
    from research_assistant.exceptions import OutputWriteError

    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr(
        "sys.argv", ["research", "summarize", str(note), "--save"]
    )

    def failing_save(*args, **kwargs):
        raise OutputWriteError("Failed to save output to outputs: Permission denied")

    monkeypatch.setattr("research_assistant.cli.save_output", failing_save)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "Failed to save output" in captured.err
