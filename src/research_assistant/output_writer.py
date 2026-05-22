"""Output writer module - saves AI output to files."""

from pathlib import Path

from research_assistant.exceptions import OutputWriteError
from research_assistant.logger import get_logger

DEFAULT_OUTPUT_DIR = "outputs"


def generate_output_filename(command: str, input_filename: str) -> str:
    """Generate an output filename based on command and input filename.

    Args:
        command: The command name (summarize, ask, tasks).
        input_filename: The input filename without path.

    Returns:
        The output filename in format: {input_filename}_{command}.md
    """
    stem = Path(input_filename).stem
    return f"{stem}_{command}.md"


def save_output(
    content: str,
    command: str,
    input_filename: str,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> str:
    """Save AI output to a Markdown file.

    Args:
        content: The content to save.
        command: The command name (summarize, ask, tasks).
        input_filename: The input filename (can include path).
        output_dir: The output directory (default: 'outputs').

    Returns:
        The path to the saved file.

    Raises:
        OutputWriteError: If the file cannot be saved.
    """
    logger = get_logger()

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filename = generate_output_filename(command, Path(input_filename).name)
        filepath = output_path / filename

        filepath.write_text(content, encoding="utf-8")
        logger.debug("Output saved to: %s", filepath)
        return str(filepath)
    except OSError as e:
        raise OutputWriteError(f"Failed to save output to {output_dir}: {e}") from e
