"""Tests for prompts module."""

from research_assistant.prompts import QA_PROMPT, SUMMARY_PROMPT, TASKS_PROMPT, format_prompt


def test_summary_prompt_contains_placeholder():
    """Test that SUMMARY_PROMPT has a {text} placeholder."""
    assert "{text}" in SUMMARY_PROMPT


def test_qa_prompt_contains_placeholders():
    """Test that QA_PROMPT has {text} and {question} placeholders."""
    assert "{text}" in QA_PROMPT
    assert "{question}" in QA_PROMPT


def test_tasks_prompt_contains_placeholder():
    """Test that TASKS_PROMPT has a {text} placeholder."""
    assert "{text}" in TASKS_PROMPT


def test_format_prompt_summary():
    """Test formatting the summary prompt."""
    result = format_prompt(SUMMARY_PROMPT, text="Hello world")
    assert "Hello world" in result
    assert "{text}" not in result


def test_format_prompt_qa():
    """Test formatting the QA prompt."""
    result = format_prompt(QA_PROMPT, text="Some text", question="What?")
    assert "Some text" in result
    assert "What?" in result
    assert "{text}" not in result
    assert "{question}" not in result


def test_format_prompt_tasks():
    """Test formatting the tasks prompt."""
    result = format_prompt(TASKS_PROMPT, text="Some text")
    assert "Some text" in result
    assert "{text}" not in result
