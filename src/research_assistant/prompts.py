"""Prompt templates for AI Research Assistant."""

SUMMARY_PROMPT = """Please summarize the following text in 2-3 sentences:

{text}

Summary:"""

QA_PROMPT = """Based on the following text, answer the question.

Text:
{text}

Question: {question}

Answer:"""

TASKS_PROMPT = """Based on the following text, generate 3 follow-up study tasks.

Text:
{text}

Study Tasks:"""


def format_prompt(template: str, **kwargs: str) -> str:
    """Format a prompt template with the given arguments.

    Args:
        template: The prompt template string with {placeholders}.
        **kwargs: Values to fill in the placeholders.

    Returns:
        The formatted prompt string.
    """
    return template.format(**kwargs)
