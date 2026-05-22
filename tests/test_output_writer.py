"""Tests for output_writer module."""

from pathlib import Path

import pytest

from research_assistant.output_writer import (
    DEFAULT_OUTPUT_DIR,
    generate_output_filename,
    save_output,
)


def test_generate_output_filename_summarize():
    """Test filename generation for summarize command."""
    result = generate_output_filename("summarize", "sample_note.md")
    assert result == "sample_note_summarize.md"


def test_generate_output_filename_ask():
    """Test filename generation for ask command."""
    result = generate_output_filename("ask", "sample_note.md")
    assert result == "sample_note_ask.md"


def test_generate_output_filename_tasks():
    """Test filename generation for tasks command."""
    result = generate_output_filename("tasks", "sample_note.md")
    assert result == "sample_note_tasks.md"


def test_generate_output_filename_txt():
    """Test filename generation with .txt input."""
    result = generate_output_filename("summarize", "notes.txt")
    assert result == "notes_summarize.md"


def test_save_output_creates_file(tmp_path):
    """Test that save_output creates a file."""
    output_dir = str(tmp_path / "outputs")
    result = save_output("Test content", "summarize", "test.md", output_dir)
    assert Path(result).exists()


def test_save_output_creates_directory(tmp_path):
    """Test that save_output creates the output directory."""
    output_dir = str(tmp_path / "new_dir" / "outputs")
    save_output("Test content", "summarize", "test.md", output_dir)
    assert Path(output_dir).exists()


def test_save_output_content(tmp_path):
    """Test that saved file has correct content."""
    output_dir = str(tmp_path / "outputs")
    content = "# Test\n\nThis is test content."
    result = save_output(content, "summarize", "test.md", output_dir)
    saved_content = Path(result).read_text(encoding="utf-8")
    assert saved_content == content


def test_save_output_returns_path(tmp_path):
    """Test that save_output returns the file path."""
    output_dir = str(tmp_path / "outputs")
    result = save_output("Test content", "summarize", "test.md", output_dir)
    assert isinstance(result, str)
    assert result.endswith(".md")


def test_save_output_filename_format(tmp_path):
    """Test that saved filename follows the expected format."""
    output_dir = str(tmp_path / "outputs")
    result = save_output("Test content", "summarize", "sample_note.md", output_dir)
    filename = Path(result).name
    assert filename == "sample_note_summarize.md"


def test_save_output_with_path_in_filename(tmp_path):
    """Test that save_output handles input filename with path."""
    output_dir = str(tmp_path / "outputs")
    result = save_output("Test content", "ask", "/path/to/note.md", output_dir)
    filename = Path(result).name
    assert filename == "note_ask.md"


def test_default_output_dir():
    """Test that DEFAULT_OUTPUT_DIR is 'outputs'."""
    assert DEFAULT_OUTPUT_DIR == "outputs"
