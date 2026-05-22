"""Output writer module - saves AI output to files."""

from pathlib import Path

DEFAULT_OUTPUT_DIR = "outputs"


def generate_output_filename(command: str, input_filename: str) -> str:
    """Generate an output filename based on command and input filename.

    Args:
        command: The command name (summarize, ask, tasks).
        input_filename: The input filename without path.

    Returns:
        The output filename in format: {input_filename}_{command}.md
    """
    # Remove extension from input filename
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
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = generate_output_filename(command, Path(input_filename).name)
    filepath = output_path / filename

    # Write content to file
    filepath.write_text(content, encoding="utf-8")

    return str(filepath)
