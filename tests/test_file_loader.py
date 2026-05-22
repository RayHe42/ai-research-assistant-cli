"""Tests for file_loader module."""

import pytest

from research_assistant.exceptions import FileLoadError
from research_assistant.file_loader import load_file


def test_load_txt_file(tmp_path):
    """Test loading a .txt file."""
    file = tmp_path / "notes.txt"
    file.write_text("Hello, world!")
    result = load_file(str(file))
    assert result == "Hello, world!"


def test_load_md_file(tmp_path):
    """Test loading a .md file."""
    file = tmp_path / "notes.md"
    file.write_text("# Title\n\nSome content here.")
    result = load_file(str(file))
    assert result == "# Title\n\nSome content here."


def test_load_file_not_found():
    """Test that FileLoadError is raised for missing files."""
    with pytest.raises(FileLoadError, match="File not found"):
        load_file("/nonexistent/file.txt")


def test_load_unsupported_extension(tmp_path):
    """Test that FileLoadError is raised for unsupported file types."""
    file = tmp_path / "data.csv"
    file.write_text("a,b,c")
    with pytest.raises(FileLoadError, match="Unsupported file type"):
        load_file(str(file))


def test_load_empty_file(tmp_path):
    """Test that FileLoadError is raised for empty files."""
    file = tmp_path / "empty.txt"
    file.write_text("")
    with pytest.raises(FileLoadError, match="empty"):
        load_file(str(file))


def test_load_whitespace_only_file(tmp_path):
    """Test that FileLoadError is raised for whitespace-only files."""
    file = tmp_path / "whitespace.txt"
    file.write_text("   \n\t  \n  ")
    with pytest.raises(FileLoadError, match="empty"):
        load_file(str(file))
