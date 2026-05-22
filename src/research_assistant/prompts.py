"""Prompt templates and builders for AI Research Assistant."""

# Output format instructions
SUMMARY_FORMAT = """## Output Format

Respond in the following Markdown format:

## Summary

[2-3 sentence summary of the main ideas]

## Key Points

- [Key point 1]
- [Key point 2]
- [Key point 3]

## Terms

- [Important term 1]: [Brief definition]
- [Important term 2]: [Brief definition]

## Follow-up Questions

1. [Question for further exploration]
2. [Question for deeper understanding]
"""

QA_FORMAT = """## Output Format

Respond in the following Markdown format:

## Answer

[Clear answer based on the note]

## Evidence from the Note

> [Relevant quote or paraphrase from the note]

## Caveats

- [Limitation or assumption in the answer]
- [If information is insufficient, state: "The note does not contain enough information to fully answer this question."]
"""

TASKS_FORMAT = """## Output Format

Respond in the following Markdown format:

## Learning Tasks

1. [Reading] [Task description]
2. [Writing] [Task description]
3. [Practice] [Task description]

## Suggested Order

- Start with: [Task 1] because [reason]
- Then: [Task 2] because [reason]
- Finally: [Task 3] because [reason]

## Estimated Difficulty

- Task 1: [Easy/Medium/Hard]
- Task 2: [Easy/Medium/Hard]
- Task 3: [Easy/Medium/Hard]
"""


def build_summarize_prompt(note_text: str) -> str:
    """Build a prompt for summarizing a note.

    Args:
        note_text: The content of the note to summarize.

    Returns:
        A formatted prompt string with task, content, constraints, and output format.
    """
    return f"""You are a research assistant helping with study notes.

## Task

Summarize the following note in a clear, structured format.

## Constraints

- Only use information from the note below
- If the note is empty or unclear, state: "The note content is insufficient to generate a summary."
- Keep the summary concise (2-3 sentences)
- Extract 3-5 key points
- Identify important technical terms
- Generate 2 follow-up questions for deeper exploration

## Note Content

{note_text}

{SUMMARY_FORMAT}"""


def build_qa_prompt(note_text: str, question: str) -> str:
    """Build a prompt for answering a question about a note.

    Args:
        note_text: The content of the note.
        question: The question to answer.

    Returns:
        A formatted prompt string with task, content, constraints, and output format.
    """
    return f"""You are a research assistant helping with study notes.

## Task

Answer the following question based on the note provided.

## Constraints

- Only use information from the note below
- If the note does not contain enough information, clearly state this in the Caveats section
- Quote or paraphrase the relevant parts of the note as evidence
- Be specific and precise in your answer

## Note Content

{note_text}

## Question

{question}

{QA_FORMAT}"""


def build_tasks_prompt(note_text: str) -> str:
    """Build a prompt for generating learning tasks from a note.

    Args:
        note_text: The content of the note.

    Returns:
        A formatted prompt string with task, content, constraints, and output format.
    """
    return f"""You are a research assistant helping with study notes.

## Task

Generate 3 follow-up learning tasks based on the note provided.

## Constraints

- Only use information from the note below
- If the note is empty or unclear, state: "The note content is insufficient to generate learning tasks."
- Include one task from each category: Reading, Writing, Practice
- Tasks should be specific and actionable
- Estimate difficulty based on the complexity of the note content

## Note Content

{note_text}

{TASKS_FORMAT}"""


# Legacy format_prompt function for backward compatibility
def format_prompt(template: str, **kwargs: str) -> str:
    """Format a prompt template with the given arguments.

    Args:
        template: The prompt template string with {placeholders}.
        **kwargs: Values to fill in the placeholders.

    Returns:
        The formatted prompt string.
    """
    return template.format(**kwargs)
