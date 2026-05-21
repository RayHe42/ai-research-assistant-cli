"""File loader module - reads .txt and .md files."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_file(filepath: str) -> str:
    """Read a text file and return its content.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {path.suffix}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    return path.read_text(encoding="utf-8")
