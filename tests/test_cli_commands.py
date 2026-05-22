"""Tests for CLI commands (happy paths)."""

import logging

import pytest

from research_assistant.cli import main
from research_assistant.logger import LOGGER_NAME


@pytest.fixture(autouse=True)
def reset_logger():
    """Reset logger state between tests to avoid handler leaks."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    yield
    logger.handlers.clear()


def test_summarize_mock_output(monkeypatch, tmp_path, capsys):
    """Test summarize command returns mock output in mock mode."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "summarize", str(note)])
    main()
    captured = capsys.readouterr()
    assert "[Mock Summary]" in captured.out


def test_ask_mock_output(monkeypatch, tmp_path, capsys):
    """Test ask command returns mock output in mock mode."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "ask", str(note), "What is this?"])
    main()
    captured = capsys.readouterr()
    assert "[Mock Answer]" in captured.out


def test_tasks_mock_output(monkeypatch, tmp_path, capsys):
    """Test tasks command returns mock output in mock mode."""
    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "tasks", str(note)])
    main()
    captured = capsys.readouterr()
    assert "[Mock Tasks]" in captured.out


def test_history_output(monkeypatch, capsys):
    """Test history command shows placeholder message."""
    monkeypatch.setattr("sys.argv", ["research", "history"])
    main()
    captured = capsys.readouterr()
    assert "No history" in captured.out


def test_no_command_shows_help(monkeypatch, capsys):
    """Test that running without a subcommand shows help."""
    monkeypatch.setattr("sys.argv", ["research"])
    main()
    captured = capsys.readouterr()
    assert "AI Research Assistant" in captured.out


def test_save_creates_file(monkeypatch, tmp_path):
    """Test that --save flag creates output file."""
    from pathlib import Path

    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "summarize", str(note), "--save"])

    output_dir = tmp_path / "outputs"
    monkeypatch.chdir(tmp_path)

    main()

    saved_file = output_dir / "note_summarize.md"
    assert saved_file.exists()
    assert "[Mock Summary]" in saved_file.read_text()


def test_ask_with_save(monkeypatch, tmp_path):
    """Test that ask --save creates output file."""
    from pathlib import Path

    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr(
        "sys.argv", ["research", "ask", str(note), "What?", "--save"]
    )
    monkeypatch.chdir(tmp_path)

    main()

    saved_file = tmp_path / "outputs" / "note_ask.md"
    assert saved_file.exists()
    assert "[Mock Answer]" in saved_file.read_text()


def test_tasks_with_save(monkeypatch, tmp_path):
    """Test that tasks --save creates output file."""
    from pathlib import Path

    note = tmp_path / "note.md"
    note.write_text("# Test\nSome content here.")
    monkeypatch.setenv("RESEARCH_ASSISTANT_MODE", "mock")
    monkeypatch.setattr("sys.argv", ["research", "tasks", str(note), "--save"])
    monkeypatch.chdir(tmp_path)

    main()

    saved_file = tmp_path / "outputs" / "note_tasks.md"
    assert saved_file.exists()
    assert "[Mock Tasks]" in saved_file.read_text()
