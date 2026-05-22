"""File loader module - reads .txt and .md files."""

from pathlib import Path

from research_assistant.exceptions import FileLoadError

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_file(filepath: str) -> str:
    """Read a text file and return its content.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file content as a string.

    Raises:
        FileLoadError: If the file does not exist, is unsupported, or is empty.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileLoadError(f"File not found: {filepath}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise FileLoadError(
            f"Unsupported file type: {path.suffix}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    content = path.read_text(encoding="utf-8")

    if not content.strip():
        raise FileLoadError(f"File is empty: {filepath}")

    return content
