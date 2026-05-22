"""Tests for prompts module."""

import pytest

from research_assistant.prompts import (
    QA_FORMAT,
    SUMMARY_FORMAT,
    TASKS_FORMAT,
    build_qa_prompt,
    build_summarize_prompt,
    build_tasks_prompt,
    format_prompt,
)


# Tests for build_summarize_prompt

def test_build_summarize_prompt_contains_task():
    """Test that summarize prompt contains task description."""
    prompt = build_summarize_prompt("Test note content")
    assert "## Task" in prompt
    assert "Summarize" in prompt


def test_build_summarize_prompt_contains_note_text():
    """Test that summarize prompt contains the note text."""
    prompt = build_summarize_prompt("Test note content")
    assert "Test note content" in prompt


def test_build_summarize_prompt_contains_constraints():
    """Test that summarize prompt contains constraints."""
    prompt = build_summarize_prompt("Test note content")
    assert "## Constraints" in prompt
    assert "Only use information from the note" in prompt


def test_build_summarize_prompt_contains_output_format():
    """Test that summarize prompt contains output format instructions."""
    prompt = build_summarize_prompt("Test note content")
    assert "## Summary" in prompt
    assert "## Key Points" in prompt
    assert "## Terms" in prompt
    assert "## Follow-up Questions" in prompt


def test_build_summarize_prompt_empty_text():
    """Test that summarize prompt handles empty text."""
    prompt = build_summarize_prompt("")
    assert "## Task" in prompt
    assert "## Constraints" in prompt


# Tests for build_qa_prompt

def test_build_qa_prompt_contains_task():
    """Test that QA prompt contains task description."""
    prompt = build_qa_prompt("Test note", "What is this?")
    assert "## Task" in prompt
    assert "Answer" in prompt


def test_build_qa_prompt_contains_note_text():
    """Test that QA prompt contains the note text."""
    prompt = build_qa_prompt("Test note content", "What is this?")
    assert "Test note content" in prompt


def test_build_qa_prompt_contains_question():
    """Test that QA prompt contains the question."""
    prompt = build_qa_prompt("Test note", "What is this about?")
    assert "What is this about?" in prompt


def test_build_qa_prompt_contains_constraints():
    """Test that QA prompt contains constraints."""
    prompt = build_qa_prompt("Test note", "What is this?")
    assert "## Constraints" in prompt
    assert "Only use information from the note" in prompt


def test_build_qa_prompt_contains_output_format():
    """Test that QA prompt contains output format instructions."""
    prompt = build_qa_prompt("Test note", "What is this?")
    assert "## Answer" in prompt
    assert "## Evidence from the Note" in prompt
    assert "## Caveats" in prompt


# Tests for build_tasks_prompt

def test_build_tasks_prompt_contains_task():
    """Test that tasks prompt contains task description."""
    prompt = build_tasks_prompt("Test note content")
    assert "## Task" in prompt
    assert "learning tasks" in prompt


def test_build_tasks_prompt_contains_note_text():
    """Test that tasks prompt contains the note text."""
    prompt = build_tasks_prompt("Test note content")
    assert "Test note content" in prompt


def test_build_tasks_prompt_contains_constraints():
    """Test that tasks prompt contains constraints."""
    prompt = build_tasks_prompt("Test note content")
    assert "## Constraints" in prompt
    assert "Only use information from the note" in prompt


def test_build_tasks_prompt_contains_output_format():
    """Test that tasks prompt contains output format instructions."""
    prompt = build_tasks_prompt("Test note content")
    assert "## Learning Tasks" in prompt
    assert "## Suggested Order" in prompt
    assert "## Estimated Difficulty" in prompt


def test_build_tasks_prompt_empty_text():
    """Test that tasks prompt handles empty text."""
    prompt = build_tasks_prompt("")
    assert "## Task" in prompt
    assert "## Constraints" in prompt


# Tests for format constants

def test_summary_format_contains_sections():
    """Test that SUMMARY_FORMAT contains required sections."""
    assert "## Summary" in SUMMARY_FORMAT
    assert "## Key Points" in SUMMARY_FORMAT
    assert "## Terms" in SUMMARY_FORMAT
    assert "## Follow-up Questions" in SUMMARY_FORMAT


def test_qa_format_contains_sections():
    """Test that QA_FORMAT contains required sections."""
    assert "## Answer" in QA_FORMAT
    assert "## Evidence from the Note" in QA_FORMAT
    assert "## Caveats" in QA_FORMAT


def test_tasks_format_contains_sections():
    """Test that TASKS_FORMAT contains required sections."""
    assert "## Learning Tasks" in TASKS_FORMAT
    assert "## Suggested Order" in TASKS_FORMAT
    assert "## Estimated Difficulty" in TASKS_FORMAT


# Legacy tests for format_prompt

def test_format_prompt_basic():
    """Test basic format_prompt functionality."""
    template = "Hello {name}, welcome to {place}!"
    result = format_prompt(template, name="Alice", place="Wonderland")
    assert result == "Hello Alice, welcome to Wonderland!"


def test_format_prompt_no_placeholders():
    """Test format_prompt with no placeholders."""
    template = "No placeholders here."
    result = format_prompt(template)
    assert result == "No placeholders here."
